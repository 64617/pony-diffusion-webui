import launch
import git
import gdown
from pathlib import Path

extension_dir = Path(__file__).parent
extension_repo = git.Repo(extension_dir)
ddb_dir = extension_dir/'deepderpibooru'
ddb_repo = extension_repo.submodules[0]
ddb_repo.update() # submodule pull in case not installed

if not Path(ddb_dir/'model.torch').exists():
    print('Downloading deepderpibooru...')
    model_fname = Path(gdown.download(id='1GTzbPoIKzjd3rsGM4WgmwKG-MOt-OMWs'))
    model_fname.rename(ddb_dir/'model.torch')
