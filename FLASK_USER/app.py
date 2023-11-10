from flask import Flask, render_template, request, session
import sqlite3 

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
            con = sqlite3.connect("member.db")
            cursor = con.cursor()
            sql = "select id, pwd from member where id = ?"
            cursor.execute(sql, (id, ))
            rows = cursor.fetchall()
            cursor.close()
            con.close()
            
            for rs in rows:
                print(rs)
                if id == rs[0] and pwd == rs[1]:
                    
                    session['logFlag'] = True
                    session['id'] = id
                
                    return render_template('main.html')
            
                else:
                    return '존재하지 않습니다. 다시 입력해주세요!' + render_template('user.html')
                
    return '존재하지 않습니다. 다시 입력해주세요!' + render_template('user.html')
            


@app.route('/logout')
def logout():
    session.clear()
    return render_template('user.html')




app.secret_key = 'sample_secret_key'




if __name__ == '__main__':
    app.run(debug=True) 

