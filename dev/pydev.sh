export PYTHONDONTWRITEBYTECODE=1
venv_name="venv"
if [ $1 ]
then
    venv_name=$1
fi
python3 -m venv ${venv_name}
source ${venv_name}/bin/activate
python3 -m pip install --upgrade pip
if [ -e ../requirements.txt ]
then
    python3 -m pip install -r ../requirements.txt
elif [ -e requirements.txt ]
then
    python3 -m pip install -r requirements.txt
fi