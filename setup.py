import os 
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from tempfile import TemporaryDirectory


cwd = os.path.dirname(os.path.abspath(__file__))

with open('requirements.txt') as f:
    reqs = f.read().splitlines()
class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        os.system('python -m unidic download')


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        os.system('python -m unidic download')

setup(
    name='melotts',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=reqs,
    package_data={
        '': ['*.txt', 'cmudict_*'],
    },
    entry_points={
        "console_scripts": [
            "melotts = melo.main:main",
            "melo = melo.main:main",
            "melo-ui = melo.app:main",
        ],
    },
)

# download model to /data/model_cache
from melo.api import TTS
try:
    engine = TTS(language='ZH', device='cuda:0', config_path='./work/data/' ,ckpt_path='./work/data/model_cache')
    speaker_ids = engine.hps.data.spk2id
    speak_speed = 1.0
    word = "准备好开始了"
    with TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, 'temp.wav')
        engine.tts_to_file(word, speaker_ids['ZH'], temp_file, speed=speak_speed)
except Exception as e:
    print(e)
    print("Failed to download model, please check your network connection and try again.")