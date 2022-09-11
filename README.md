# Yuriy Zhagan Junior Python Developer Test Task
```
██████   █████  ████████  █████         ██████  ██   ██ 
██   ██ ██   ██    ██    ██   ██       ██    ██  ██ ██  
██   ██ ███████    ██    ███████ █████ ██    ██   ███   
██   ██ ██   ██    ██    ██   ██       ██    ██  ██ ██  
██████  ██   ██    ██    ██   ██        ██████  ██   ██ 
```

## Requirements
- python 3.10
- postgresql 14.5
- Docker(optional)

## Installation
```bash
git clone https://github.com/yurijGagarin/data_ox_test_task.git
cd data_ox_test_task
cp .env.example .env
# edit .env
```

## Local env
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Apply migrations
```bash
alembic upgrade head
```

###  Run app
    
```bash
python -m parser.main
```

## Docker
```bash
docker-compose up
```

## Database Dump File
`dump.sql`