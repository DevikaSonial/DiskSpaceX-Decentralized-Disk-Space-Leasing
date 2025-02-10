from flask import *

from database import *

public=Blueprint("public",__name__)



@public.route('/')
def home_page():
    return render_template('home.html')



@public.route('/login',methods=['get','post'])
def login():
    if 'login' in request.form:
        uname=request.form['uname']
        password=request.form['pwd']

        qry="select * from login where username='%s' and password ='%s'"%(uname,password)
        res=select(qry)

        if res:
            session['login_id']=res[0]['login_id']

            if res[0]['usertype']=='admin':
                return ("<script>alert('login successfull');window.location='/admin_home'</script>")
                            
            if res[0]['usertype']=='user':

                qrt="select * from user where login_id='%s'"%(session['login_id'])
                res2=select(qrt)

                if res2:
                    session['user_id']=res2[0]['user_id']
                    session['uname']=res2[0]['fname']

                return ("<script>alert('login successfull');window.location='/users_home'</script>")
            
        else:
            return ("<script>alert('Invalid Username or Password ');window.location='/login'</script>")

    return render_template('login.html')



@public.route('/public_user_register',methods=['get','post'])
def public_user_register():

    if 'send' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        phone=request.form['ph']
        email=request.form['mail']
        uname=request.form['uname']
        pwd=request.form['pwd']


        qrt="insert into login values(null,'%s','%s','user')"%(uname,pwd)
        loginid=insert(qrt)

        qry="insert into `user` values (null,'%s','%s','%s','%s','%s')"%(loginid,fname,lname,phone,email)
        res=insert(qry)

        return ("<script>alert('Register Successfully');window.location='/login'</script>")


    return render_template('public_user_register.html')