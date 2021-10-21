from flask import Flask, render_template, request, redirect, session, flash
import json

app = Flask(__name__)
app.secret_key = 'IU+ta5:9~0vZ,*}'


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Conta:
    def __init__(self, usuario, senha):
        self.usuario = usuario
        self.senha = senha


lista = [
    Jogo('Tetris', 'Estratégia', 'GameBoy'),
    Jogo('Sonic', 'Aventura', 'GameBoy'),
    Jogo('Contra', 'Ação', 'GameBoy')
]

contas = [
    Conta('usuario_01', 'usuario_01'),
    Conta('usuario_02', 'usuario_02'),
    Conta('usuario_03', 'usuario_03')
]


@app.route('/')
def render_lista_jogos():
    if 'usuario_logado' not in session or session.get('usuario_logado') == None:
        return redirect('/login')
    return render_template(
        'lista.html',
        page_title='Jogoteca',
        titulo='Jogos',
        jogos=lista
    )


@app.route('/novo')
def render_cadastro_jogo():
    if 'usuario_logado' not in session or session.get('usuario_logado') == None:
        return redirect('/login')
    return render_template(
        'novo.html',
        titulo='Jogoteca'
    )


@app.route('/create', methods=['POST'])
def create_jogo():
    lista.append(
        Jogo(
            request.form['nome'],
            request.form['categoria'],
            request.form['console']
        )
    )
    return redirect('/')


@app.route('/login')
def login():
    if 'usuario_logado' in session and session.get('usuario_logado') is not None:
        return redirect('/')
    return render_template('login.html')


@app.route('/autenticar', methods=['POST'])
def autenticar():
    matches = [
        conta
        for conta in contas
        if conta.usuario == request.form['senha']
           and conta.usuario == request.form['usuario']
    ]
    if len(matches) == 1:
        session['usuario_logado'] = json.dumps(matches[0].__dict__)
        return redirect('/')
    else:
        flash('Usuário e(ou) senha inválido(s)!')
        return redirect('login')


@app.route('/desautenticar')
def deslogar():
    session['usuario_logado'] = None
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
