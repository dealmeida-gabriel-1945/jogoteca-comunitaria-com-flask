from flask import Flask, render_template, request, redirect, session, flash
import json
from types import SimpleNamespace

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
        self.jogos = []

    def as_dict(self):
        dict = self.__dict__
        dict["jogos"] = [jogo.__dict__ for jogo in dict["jogos"]]
        return dict


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
        jogos=get_usuario_logado().jogos
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
    usuario_logado = get_usuario_logado()
    usuario_logado.jogos.append(
        Jogo(
            request.form['nome'],
            request.form['categoria'],
            request.form['console']
        )
    )
    save_usuario_logado(usuario_logado)
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
        if conta.usuario == request.form['usuario']
           and conta.senha == request.form['senha']
    ]
    if len(matches) == 1:
        session['usuario_logado'] = json.dumps(parse_conta_from_session(matches[0]).as_dict())
        return redirect('/')
    else:
        flash('Usuário e(ou) senha inválido(s)!')
        return redirect('login')


@app.route('/desautenticar')
def deslogar():
    session['usuario_logado'] = None
    return redirect('/login')


def get_usuario_logado():
    return json.loads(
        session['usuario_logado'],
        object_hook=lambda d: SimpleNamespace(**d)
    )


def save_usuario_logado(to_save):
    conta_aux = Conta(to_save.usuario, to_save.senha)
    conta_aux.jogos = to_save.jogos
    session['usuario_logado'] = json.dumps(conta_aux.as_dict())
    aux = list()
    for conta in contas:
        if conta.usuario == to_save.usuario and conta.senha == to_save.senha:
           aux.append(to_save)
        else:
            aux.append(conta)
    contas.clear()
    contas.extend(aux)
    print('conta salva')


def parse_conta_from_session(to_parse):
    to_return = Conta(to_parse.usuario, to_parse.senha)
    to_return.jogos = to_parse.jogos
    return to_return


if __name__ == '__main__':
    app.run(debug=True)
