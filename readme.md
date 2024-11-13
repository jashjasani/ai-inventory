# Dependencies 

- [Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/)
- Get a fireworks API key and add it to .env file as shown in .env.example  [Fireworks](https://fireworks.ai/account/)

# Installation 

```bash 
git clone https://github.com/jashjasani/ai-inventory.git
cd ai-inventory
conda create -p ./venv python=3.10.0 && conda activate ./venv
pip install -r requirements.txt
```

# Start server 
Inside ai-inventory directory
```bash 
fastapi dev app.py
```

This will start a server on http://127.0.0.1:8000 <br>
You can access the API documentation at http://127.0.0.1:8000/docs to learn how to use it.
