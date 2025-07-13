from module.api import Script
from typing import Annotated

import os
import logging
import subprocess
import libtorrent as bt
from pathlib import Path

class Torrent2Magnet(Script):
    def __get_magnet(self, filepath : Path):
        if not filepath.exists() or filepath.suffix != '.torrent':
            return None
        info = bt.torrent_info(str(filepath))
        magnet = f"magnet:?xt=urn:btih:{info.info_hash()}&dn={info.name()}"
        return magnet
    """将种子文件转为磁力链接"""
    def run(self, path: Annotated[str, "种子文件夹或文件"], remove: Annotated[bool, "完成后是否删除种子文件"] = False):
        path = Path(path)
        res = []
        if path.is_dir():
            for filepath in path.glob("*.torrent"):
                magnet = self.__get_magnet(filepath)
                res.append(magnet)
                # 清除种子
                if remove:
                    subprocess.run(["trash", filepath])
        elif path.is_file() and path.suffix == '.torrent':
            magnet = self.__get_magnet(path)
            res.append(magnet)
            # 清除种子
            if remove:
                subprocess.run(["trash", path])
        else:
            logging.warning(f"文件或路径不合法 : {path}")
            return
        subprocess.run("pbcopy", universal_newlines=True, input="\n".join(res))
        subprocess.run(["open", "raycast://confetti"])