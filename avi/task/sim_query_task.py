"""
Copyright (C) 2016-2020 Quasar Science Resources, S.L.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.

@package avi.task.sim_query_task

--------------------------------------------------------------------------------

This module manages the execution of queries to the simulations server.

The module manages the execution of queries to the simulations server.
"""
import time
import sys, traceback, os
from django.utils import timezone

import shutil, urllib, ssl

try:
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    url_lib = urllib.request
except ImportError:
    from urllib2 import Request, urlopen
    from urllib import urlencode
    url_lib = urllib2

import bs4
import tarfile
import shutil

from .task import task as parent
from .task import task_exception as err

from avi.log import logger

from avi.core.risea import risea
from avi.core.interface.interface_manager import interface_manager
from avi.utils.data.file_manager import file_manager
from avi.utils.data.json_manager import json_manager
from avi.warehouse import wh_global_config as wh

class sim_query_task(parent):
    """@class sim_query_task
    The sim_query_task class manages the execution of queries to the simulations 
    server.

    It implementes the task interface and inherits the task_data attribute.

    @see task @link avi.task.task.task
    @see task_data @link avi.task.task.task_data
    """
    def output(self):
        """Deprecated"""
        pass

    def total_mass_2_str(self, num):
        ret = ""
        try:
            dat = str(int(num))
            ret = "Total_Mass_" + dat + "Msun/"
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret

    def virial_ratio_2_str(self, num):
        ret = ""
        try:
            dat = int(num * 10)
            if dat == 5:
                ret = "Virial_equilibrium_Q0p5/"
            if dat == 3:
                ret = "Virially_cold_Q0p3/"
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret

    def half_mass_radius_2_str(self, num):
        ret = ""
        try:
            dat = int(num * 10)
            if dat < 10:
                ret = "Rh" + str(dat).zfill(2) + "/"
            else:
                ret = "Rh" + str(dat) + "/"
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret

    def fractal_dimension_2_str(self, num):
        ret = ""
        try:
            dat = int(num * 10)
            ret = "D" + str(dat).zfill(2)
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret

    def segregation_degree_2_str(self, num):
        ret = ""
        try:
            dat = int(num * 10)
            ret = "S" + str(dat).zfill(2)
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret
    def binary_fraction_2_str(self, num):
        ret = ""
        try:
            dat = int(num * 10)
            ret = "bin" + str(dat).zfill(2)
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret
    def total_mass_2_str_name(self, num):
        ret = ""
        try:
            dat = str(int(num))
            ret = "M10" + str(len(dat) - 1)
        except Exception:
            return ""
        finally:
            if ret == "":
                return ret
        return ret
    def half_mass_radius_2_str_name(self, num):
        ret = ""
        try:
            dat = int(num * 10)
            ret = "r" + str(dat).zfill(2)
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret
    def virial_ratio_2_str_name(self, num):
        ret = ""
        try:
            dat = int(num * 10)
            ret = "Q" + str(dat).zfill(2) + "/"
        except Exception:
            return ""
        finally:
            if ret == "":
                return ""
        return ret

    def download_file(self, url, path):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urlopen(url, context=ctx)
        file_name = url[url.rindex("/", 0, len(url)) + 1:]
        print(os.path.join(path, file_name))
        fp = open(os.path.join(path, file_name), 'wb')
        shutil.copyfileobj(response, fp)
        fp.close()

    def parse_url(self, url, path):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urlopen(url, context=ctx)
            data = bs4.BeautifulSoup(response.read(), "html.parser")
            for l in data.find_all("a"):
                ldat = l['href']
                if ldat[0] == '?' or ldat[0] == '/':
                    continue
                if ldat[len(ldat) - 1] == '/':
                    #print("directory " + url + l['href'])
                    new_url = url + l['href']
                    new_dir = new_url[new_url.rindex("/", 0, len(new_url) - 1)+1:-1]
                    os.mkdir(os.path.join(path, new_dir))
                    try:
                        self.parse_url(new_url, os.path.join(path, new_dir))
                    except urllib.error.HTTPError as e:
                        if e.code == "404":
                            continue
                    except Exception:
                        continue
                #print(url + l['href'])
                else:
                    #self.file_list.append(url + l['href'])
                    try:
                        self.download_file(url + l['href'], path)
                    except urllib.error.HTTPError as e:
                        if e.code == "404":
                            continue
                    except Exception:
                        continue
        except urllib.error.HTTPError as e:
            if e.code == "404":
                return False
        except Exception as e:
            raise err('Cannot download the file')
        return True

    def run(self):
        """Runs the query to the simulations server.

        Args:
        self: The object pointer.

        Raises:
        task_exception: avi.task.task.task_exception
        """
        im = risea().get().interface_manager
        cfg = im.sim_config
        if cfg.get("url"):
            base_url = cfg["url"]
        else:
            base_url = "http://sims.starformmapper.es/files/"
            
        if cfg.get("path"):
            sub_folder = cfg["path"]
        else:
            sub_folder = "pure_nbody_sims/"
        tm = self.total_mass_2_str(self.task_data.data['total_mass'])
        vr = self.virial_ratio_2_str(self.task_data.data['virial_ratio'])
        hmr = self.half_mass_radius_2_str(self.task_data.data['half_mass_radius'])
        fd = self.fractal_dimension_2_str(self.task_data.data['fractal_dimension'])#"D30"
        sd = self.segregation_degree_2_str(self.task_data.data['mass_segregation_degree'])#"S00"
        bf = self.binary_fraction_2_str(self.task_data.data['binary_fraction'])#"bin00"
        tm_name = self.total_mass_2_str_name(self.task_data.data['total_mass'])#"M103"
        hmr_name = self.half_mass_radius_2_str_name(self.task_data.data['half_mass_radius'])#"r01"
        vr_name = self.virial_ratio_2_str_name(self.task_data.data['virial_ratio']) #"Q05/"

        url = base_url+sub_folder+tm+vr+hmr+fd+sd+bf+tm_name+hmr_name+vr_name

        print("SIMS")
        print(url)

        try:
            self.file_list = []
            risea().get()
            self.tmp_path = wh().get().TMP_PATH
            directory_name = str(round(time.time()))+"_"+fd+sd+bf+tm_name+hmr_name+vr_name
            download_path = os.path.join(self.tmp_path, directory_name)
            os.mkdir(download_path)
            ret = self.parse_url(url, download_path)
            if not ret:
                shutil.rmtree(download_path)
                return

            fm = file_manager()
            fm.save_tar_file(download_path, directory_name[:-1] + ".tar.gz", wh().get().SIM_PATH, self.task_id, "sim", timezone.now())

            #tar_name = download_path[:-1] + ".tar.gz"
            #with tarfile.open(tar_name, "w:gz") as tar:
            #    tar.add(download_path, arcname = os.path.basename(download_path))
            shutil.rmtree(download_path)

        except Exception as e:
            raise err('Cannot download the file') 
        print(self.file_list)
        return
                
