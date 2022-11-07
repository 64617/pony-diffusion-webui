import launch
import git
import gdown
from shutil import copy
from pathlib import Path

extension_dir = Path(__file__).parent
extension_repo = git.Repo(extension_dir)
for submodule in extension_repo.submodules:
    submodule.update()

##
## DDB
##
ddb_dir = extension_dir/'deepderpibooru'
if not Path(ddb_dir/'model.torch').exists():
    print('Downloading deepderpibooru...')
    model_fname = Path(gdown.download(id='1GTzbPoIKzjd3rsGM4WgmwKG-MOt-OMWs'))
    model_fname.rename(ddb_dir/'model.torch')


##
## tag complete
##
tagcomp_dir = extension_dir/'a1111-sd-webui-tagcomplete'
tagcomp_js = tagcomp_dir/'javascript'/'tagAutocomplete.js'
tagcomp_py = tagcomp_dir/'scripts'/'tag_autocomplete_helper.py'

copy(tagcomp_js, extension_dir/'javascript')
copy(tagcomp_py, extension_dir/'scripts')

