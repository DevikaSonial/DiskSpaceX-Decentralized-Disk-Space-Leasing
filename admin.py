from flask import *
from database import *



admin=Blueprint("admin",__name__)



@admin.route('/admin_home')
def admin_home():
    return render_template("admin_home.html")



@admin.route('/admin_view_users')
def admin_view_users():
    data={}

    qry="select * from  `USER` "
    res=select(qry)
    data["users"]=res
    return render_template("admin_view_users.html",data=data)



@admin.route('/admin_view_complaints')
def admin_view_complaints():
    data={}

    qry="select * from `complaints` "
    res=select(qry)
    data["complaints"]=res

    return render_template("admin_view_complaints.html",data=data)


@admin.route('/admin_send_reply',methods=['get','post'])
def admin_send_reply():

    id=request.args['id']

    if 'send' in request.form:

        reply=request.form['repl']
        qry="update  `complaints` set reply='%s' where complaints_id='%s'"%(reply,id)
        res=update(qry)

        return ("<script>alert('Send Successfully');window.location='/admin_view_complaints'</script>")
        
    return render_template('admin_send_reply.html')




@admin.route('/admin_send_notification',methods=['get','post'])
def admin_send_notification():


    if 'send' in request.form:

        title=request.form['tit']
        desc=request.form['desc']

        qry="insert into notification values(null,'%s','%s',curdate())"%(title,desc)
        res=insert(qry)
        return ("<script>alert('Send Successfully');window.location='/admin_send_notification'</script>")
        
    return render_template('admin_send_notification.html')
