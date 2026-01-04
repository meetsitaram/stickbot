
source ~/solo_venv/bin/activate


cd ~
uv venv solo_venv --python 3.12.12
source ./solo_venv/bin/activate
uv pip install -e .
