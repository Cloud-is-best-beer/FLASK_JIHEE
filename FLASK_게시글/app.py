from flask import Flask, render_template, request, session, url_for, redirect
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





### 게시글 ####

# 게시판
@app.route('/board', methods = ['GET', 'POST'])
def board():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from Board")
    rows = cur.fetchall()
    print("DB:")
    for i in range(len(rows)):
            print(rows[i][0] + ':' + rows[i][1])
    return render_template('board1.html', rows = rows)
    # board1.html에 rows값 리턴, board1.html에는 모든 row값들을 보여줘야하므로 rows
 
 
 
# 게시글 작성
@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            name = request.form['name']
            context = request.form['context']
            with sqlite3.connect("database.db") as con:
                cursor = con.cursor()
                cursor.execute(f"INSERT INTO Board (name, context) VALUES ('{name}', '{context}')")
                con.commit()
        except:
            con.rollback()
        finally : 
            con.close()
            return redirect(url_for('board'))
    else:
        return render_template('add.html')
 
 
 
 
# 게시글 업데이트
# /update/<uid> -> 해당 uid를 넣어서 주소창 생성 : 해당 uid에 관한 내용의 페이지가 나옴
@app.route("/update/<uid>", methods=["GET","POST"])
def update(uid):
    # update(uid) : uid데이터를 서버 측으로 전달
    # post방식으로 넘어가면
    if request.method == "POST":
        name = request.form["name"]
        context = request.form["context"]
        
        # 내용 갱신하고
        with sqlite3.connect("database.db") as con:
            cursor = con.cursor()  
            cursor.execute(f"UPDATE Board SET name='{name}', context='{context}' WHERE name='{uid}'")
            con.commit()
 
        return redirect(url_for('board'))  
    else:
        # 밑에 기존 내용 보여주는 코드
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute(f"SELECT * FROM Board WHERE name='{uid}'")
        row = cursor.fetchall()
        return render_template("update.html",row=row)
        # update.html 에 row값 리턴, update는 row한 줄 값만 필요하므로 row
 
 

# 게시글 삭제
@app.route("/delete/<uid>")
def delete(uid):
    # 들어온 uid 값이랑 name이랑 delete 연산하고 반영
    with sqlite3.connect("database.db") as con:
        cursor = con.cursor()
        cursor.execute(f"DELETE FROM Board WHERE name='{uid}'")
        con.commit()
 
    return redirect(url_for('board'))





app.secret_key = 'sample_secret_key'




if __name__ == '__main__':
    app.run(debug=True) 

