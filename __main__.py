import os

# Para subir o jogo no PyPi (pip3)
# No setup.py deve se lingar a essa função!
def main():
    path = os.path.dirname(__file__)
    os.chdir(path)
    os.system('pgzerun main.py')
