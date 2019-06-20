from urllib.request import Request, urlopen
import zipfile
import os
import tempfile
import shutil
import platform
import sys
import ssl


# Save chmod rules
class Zip(zipfile.ZipFile):
    def extract(self, member, path=None, pwd=None):
        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()

        ret_val = self._extract_member(member, path, pwd)
        attr = member.external_attr >> 16
        os.chmod(ret_val, attr)
        return ret_val


def dlffmpeg(ffmpegpath=os.getcwd()):

    if sys.platform == 'win32':
        if platform.machine() == 'AMD64':
            ver = 'win64'
        else:
            ver = 'win32'

    if sys.platform == 'darwin':
        ver = 'macos64'

    if sys.platform == 'linux':
        print("For linux try 'apt-get install ffmpeg'")
        return False

    context = ssl._create_unverified_context()

    url = 'https://ffmpeg.zeranoe.com/builds/{0}/static/'.format(ver)
    sort = '?C=M&O=D'
    req = Request(url+sort, headers={'User-Agent': 'Mozilla/5.0'})

    try:
        webpage = urlopen(req,context=context).read()
    except Exception as e:
        print(e)
        return False
    webpage = webpage.decode('UTF-8')

    # get file name
    a = webpage.find('ffmpeg')
    b = webpage.find('.zip')
    print(webpage[a:b+4])
    name = webpage[a:b+4]

    # make tmp folder
    with tempfile.TemporaryDirectory() as tmpdir:
        req = Request(url + name, headers={'User-Agent': 'Mozilla/5.0'})
        tmpfile = os.path.join(tmpdir, name)
        with open(tmpfile, 'wb') as f:
            try:
                f.write(urlopen(req,context=context).read())
            except Exception as e:
                print(e)
                return False

        if os.path.exists(tmpfile):
            with Zip(tmpfile, "r") as zip:
                for file in zip.namelist():
                    if file.startswith(name[:-4] + '/bin/'):
                        zip.extract(file, tmpdir)

        # cd to bin folder
        un = os.path.join(tmpdir, name[:-4],'bin')
        for file in os.listdir(un):
            print(file)
            shutil.move(
                os.path.join(un, file),
                os.path.join(ffmpegpath, file))
        return True


if __name__ == "__main__":
    dlffmpeg()
