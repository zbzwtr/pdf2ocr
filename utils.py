import pandas as pd
import numpy as np
from env import OCR_OUT
import os
from pathlib import PurePath
from ast import literal_eval
import itertools

def get_filepaths_from_folder(folder_path: str, file_ext: str):
    files = os.listdir(folder_path)
    filepaths = [
        f"./ocr/{f}"
        for f in files
        if PurePath(f).suffix == file_ext and PurePath(f).stem != "all"
    ]
    return filepaths


def get_ocr_output_fields(example_file):
    # assume tsv
    df = pd.read_csv(example_file, sep="\t", index_col=0)
    return df.columns.to_list() + ["filepath"]


def collect_ocr_outputs(folder_path, file_ext):
    filepaths = get_filepaths_from_folder(folder_path, file_ext)
    cols = get_ocr_output_fields(filepaths[0])
    df = pd.DataFrame(columns=cols)
    for fp in filepaths:
        _df = pd.read_csv(fp, sep="\t", index_col=0)
        _df["filepath"] = fp
        _df["filename"] = PurePath(fp).name
        df = pd.concat([df, _df])
    return df


def rescale_ocr_output(fp, new_img_w, new_img_h, new_fp):
    df = pd.read_csv(fp, sep="\t", index_col=0)
    old_img_h = df["image_height"].iloc[0]
    old_img_w = df["image_width"].iloc[0]
    scale_w = new_img_w / old_img_w
    scale_h = new_img_h / old_img_h
    df["image_height"] = new_img_h
    df["image_width"] = new_img_w
    df[["left", "width"]] = (df[["left", "width"]] * scale_w).round(0).astype(int)
    df[["top", "height"]] = (df[["top", "height"]] * scale_h).round(0).astype(int)
    df.to_csv(new_fp, sep="\t")


def concat_ocr_outputs(folder_path: str, file_ext: str, new_fp: str):
    # use tsv
    df = collect_ocr_outputs(folder_path, file_ext)
    df["bbox"] = df[["top", "left", "width", "height"]].values.tolist()
    df.fillna(value="", inplace=True)

    df_out = pd.DataFrame(
        columns=[
            "page_num",
            "line_num",
            "bbox",
            "conf",
            "text",
            "image_height",
            "image_width",
            "filepath"
        ]
    )
    _merge_fields = ["page_num", "line_num", "conf", "text", "filepath"]

    for fp in df["filepath"].unique():
        _df = df[df["filepath"] == fp]
        _df_out = pd.DataFrame(columns=["page_num", "line_num", "bbox", "conf", "text"])

        _df_out[_merge_fields] = [_df[_merge_fields].T.values.tolist()]
        _df_out["bbox"] = [_df["bbox"].values.tolist()]
        _df_out["filepath"] = _df["filepath"].iloc[0]
        _df_out["image_height"] = _df["image_height"].iloc[0]
        _df_out["image_width"] = _df["image_width"].iloc[0]

        df_out = pd.concat([df_out, _df_out])

    df_out['element_count'] = [len(df_out['page_num'].iloc[i]) for i in range(0, df_out.shape[0])]

    df_out.to_csv(new_fp, sep="\t")
    df_out.to_csv(new_fp[:-3] + "csv")
    return df_out


def decat_ocr_outputs(fp: str, dest_folder="./ocr"):
    def flatten_lst(lst):
        return list(itertools.chain.from_iterable(lst))
    # use tsv
    converters = {
        "page_num": pd.eval,
        "line_num": pd.eval,
        "bbox": pd.eval,
        "conf": pd.eval,
        "text": pd.eval,
    }
    df = pd.read_csv(fp, sep="\t", index_col=0, converters=converters)
    df.reset_index(inplace=True, drop=True)
    df_out = pd.DataFrame(columns=df.columns)
    
    flatten_fields = ['page_num', 'line_num', 'bbox', 'conf', 'text']
    for field in flatten_fields:
        df_out[field] = flatten_lst(df[field].values.tolist())
    
    # unpack bbox
    df_out["top"] = df_out["bbox"].str[0]
    df_out["left"] = df_out["bbox"].str[1]
    df_out["width"] = df_out["bbox"].str[2]
    df_out["height"] = df_out["bbox"].str[3]

    # et al
    single_fields = ['image_height', 'image_width', 'filepath']
    df_out[single_fields] = ['', '', '']
    running_count = 0
    for i, _count in enumerate(df['element_count']):
        df_out.loc[running_count:running_count + _count - 1, single_fields] = df.loc[i, single_fields].values
        running_count += _count

    # distribute files
    for fp in df_out['filepath'].unique():
        df = df_out[df_out["filepath"] == fp]
        df.to_csv(fp, sep='\t')
        df.to_csv(fp[:-3] + "csv")

if __name__ == "__main__":
    # df = concat_ocr_outputs(
    #     folder_path="./ocr", file_ext=".tsv", new_fp="./ocr/all.tsv"
    # )
    decat_ocr_outputs(fp="./ocr/all.tsv", dest_folder='./ocr')
    # get_filepaths_from_folder(folder_path=OCR_OUT, file_ext=".tsv")
    # rescale_ocr_output("./ocr/1.tsv", 500, 500, "./ocr/1_500x500.tsv")
