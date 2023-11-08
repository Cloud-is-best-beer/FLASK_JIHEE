from flask import Flask, render_template, request, session

app = Flask(__name__)


@app.route('/')
def new_user():
    return render_template('user.html')



@app.route('/user_info', methods = ['POST', 'GET'])
def user_info():
    if request.method == 'POST':
        id = request.form['id']
        pwd = request.form['pwd']
    
        if len(id) == 0 or len(pwd) == 0:
            return '아이디, 비밀번호를 모두 입력해주세요!' + render_template('user.html')
    
        else:
            val = request.form 
            return render_template('main.html', result=val)
            

            

@app.route('/logout')
def logout():
    session.clear()
    return render_template('user.html')



app.secret_key = 'sample_secret_key'


if __name__ == '__main__':
    app.run(debug=True) 

