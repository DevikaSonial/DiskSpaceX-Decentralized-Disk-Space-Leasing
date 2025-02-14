from datetime import date
import uuid
from flask import *
from database import *
# from spli import *
# from merge_split_files import *
from blk import *

from new import *



users=Blueprint("users",__name__)



@users.route('/users_home')
def users_home():
    return render_template("users_home.html")



@users.route('/users_view_profile')
def users_view_profile():
    data={}
    
    qry="select * from user where login_id='%s'"%(session['login_id'])
    res=select(qry)
    data['view']=res


    return render_template("users_view_profile.html",data=data)


@users.route('/user_edit_profile',methods=['get','post'])
def user_edit_profile():
    data={}

    id=request.args['id']

    qry="select * from user where user_id='%s'"%(id)
    res=select(qry)
    data['edit']=res

    if 'edit' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        phone=request.form['ph']
        email=request.form['mail']

        qrup="update user set fname='%s',lname='%s',phone='%s',email='%s' where user_id='%s'"%(fname,lname,phone,email,id)
        update(qrup)

        return ("<script>alert('Edit Successfully');window.location='/users_view_profile'</script>")


    return render_template('user_edit_profile.html',data=data)



@users.route('/user_send_complaints',methods=['get','post'])
def user_send_complaints():
    data={}

    qrty="select * from `complaints` where user_id='%s'"%(session['user_id'])
    res=select(qrty)
    data['complaints']=res


    if 'send' in request.form:
        title=request.form['tit']
        descr=request.form['desc']


        qry="insert into `complaints` values(null,'%s','%s','%s','pending',curdate())"%(session['user_id'],title,descr)
        res=insert(qry)

        return ("<script>alert('Add Successfully');window.location='/user_send_complaints'</script>")

        
    return render_template('user_send_complaints.html',data=data)


@users.route('/user_view_notification')
def user_view_notification():
    data={}

    qry="select * from notification"
    res=select(qry)
    data['notification']=res

    return render_template('user_view_notification.html',data=data)






@users.route('/user_add_system_details',methods=['get','post'])
def user_add_system_details():

    if 'send' in request.form:
        systemname=request.form['sname']
        systempassword=request.form['spass']
        systemusername=request.form['suname']
        filename=request.form['fname']

        qry="insert into `system_details` values(null,'%s','%s','%s','%s','%s')"%(session['user_id'],systemname,systempassword,systemusername,filename)
        insert(qry)
        return ("<script>alert('Add Successfully');window.location='/users_home'</script>")

    return render_template('user_add_system_details.html')


# @users.route('/user_upload_share_file', methods=['get', 'post'])
# def user_upload_share_file():
#     data={}
#     qrty=" SELECT * FROM system_details WHERE user_id != '%s' LIMIT 2;"%(session['user_id'])
#     rts=select(qrty)
#     data['view']=rts

#     print(rts,"//////////////////////")

#     system_id_1 = rts[0]['system_details_id']
#     system_id_2 = rts[1]['system_details_id']

#     print("System Details ID 1:", system_id_1)
#     print("System Details ID 2:", system_id_2)  


#     if 'send' in request.form:

#         file = request.files['file']
#         title = request.form['title']

#         # Generate and save the file
#         path = 'static/' + str(uuid.uuid4()) + file.filename
#         file.save(path)

#         print(path, "///////////////////////")
        
#         # Call the upload_file function
#         dd = upload_file(path,rts,title)

#         print(dd, "//////////////////////////+++++++++++++")

#         # Extract paths and samples
#         pathone = dd[0][2].replace("\\", "\\\\")  # Properly formatted path for part1
#         pathtwo = dd[1][2].replace("\\", "\\\\")  # Properly formatted path for part2

#         # Extract filenames (sample.zip.part1, sample.zip.part2)
#         sample1 = dd[0][0]  # Extract filename from the first tuple
#         sample2 = dd[1][0]  # Extract filename from the second tuple

#         print(pathone, "//////////++++++--------------")
#         print(pathtwo, "//////////////++++++++==================")
#         print(sample1, "//////////////++++++++ SAMPLE 1")
#         print(sample2, "//////////////++++++++ SAMPLE 2")

#         # Insert into the database

#         # qrty = """INSERT INTO `upload_file` 
#         #   VALUES (null, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', CURDATE())""" % (
#         # session['user_id'], system_id_1, system_id_2, title, pathone, pathtwo, sample1, sample2)
#         # insert(qrty)

#         from datetime import date
#         current_date = date.today()
#         print("Current date:", current_date)
#         d = current_date.strftime("%Y-%m-%d")



#         with open(compiled_contract_path) as file:
#             contract_json = json.load(file)  # load contract info as JSON
#             contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
#         contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
#         id=web3.eth.get_block_number()
#         message = contract.functions.add_upload_file(int(id),int(session['user_id']),int(system_id_1),int(system_id_2),title, pathone, pathtwo, sample1, sample2,d).transact()
#         print(message)

#         return "<script>alert('Upload Successfully');window.location='/users_home'</script>"

#     return render_template('user_upload_share_file.html',data=data)



# @users.route('/user_view_share_file')
# def user_view_share_file():
#     data={}

#     # qrty="select * from upload_file where user_id='%s'"%(session['user_id'])
#     # res=select(qrty)
#     # data['view']=res
   

#     with open(compiled_contract_path) as file:
#         contract_json = json.load(file)  # load contract info as JSON
#         contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
#     contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
#     blocknumber = web3.eth.get_block_number()
#     res = []
#     try:
#         for i in range(blocknumber, 0, -1):
#             a = web3.eth.get_transaction_by_block(i, 0)
#             decoded_input = contract.decode_function_input(a['input'])
#             print(decoded_input, "///////////////////")
#             if str(decoded_input[0]) == "<Function add_upload_file(uint256,uint256,uint256,uint256,string,string,string,string,string,string)>":
#                 if int(decoded_input[1]['user_id']) == int(session['user_id']):
#                     res.append(decoded_input[1])
#     except Exception as e:
#         print("", e)
#     data['view'] = res

#     print(res,"///////////////////+++++++++")
    
#     return render_template('user_view_share_file.html',data=data)



# @users.route('/user_retrieve_files')
# def user_retrieve_files():
#     data = {}
#     upid = request.args['upid']
    
#     # Load contract and web3 setup
#     with open(compiled_contract_path) as file:
#         contract_json = json.load(file)  # load contract info as JSON
#         contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    
#     contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
#     blocknumber = web3.eth.get_block_number()
#     res = []
    
#     try:
#         for i in range(blocknumber, 0, -1):
#             a = web3.eth.get_transaction_by_block(i, 0)
#             decoded_input = contract.decode_function_input(a['input'])
#             print(decoded_input, "///////////////////bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
#             if str(decoded_input[0]) == "<Function add_upload_file(uint256,uint256,uint256,uint256,string,string,string,string,string,string)>":
#                 if int(decoded_input[1]['upload_file_id']) == int(upid):
#                     res.append(decoded_input[1])
#     except Exception as e:
#         print("", e)
    
#     data['view'] = res

#     print(res,"//////////////////////////////0000000000000000000000000000000")
    
#     # Commented out SQL query code
#     # qry="SELECT * FROM `upload_file` WHERE `upload_file_id`='%s'"%(upid)
#     # print(qry,"qqqqqqqqqqqqqqqqqqq")
#     # res=select(qry)
#     # print("RES : ",res)
    
#     data['system_details_first_id'] = ""
#     data['system_details_second_id'] = ""
    
#     if res:
#         for i in res:
#             print(i,"/////////////////////////////////++++++++++++++++++=")

#             print(i['system_details_first_id'])
#             print(i['system_details_second_id'])
            
#             data['view'] = res
#             data['system_details_first_id'] = i['system_details_first_id']
#             data['system_details_second_id'] = i['system_details_second_id']
    
#     retrieve_files(res, data['system_details_first_id'], data['system_details_second_id'])
    
#     return "<script>alert('Retrieve Successfully');window.location='/users_home'</script>"

@users.route('/user_upload_share_file', methods=['get', 'post'])
def user_upload_share_file():
    data = {}
    qrty = " SELECT * FROM system_details WHERE user_id != '%s' LIMIT 2;" % (session['user_id'])
    rts = select(qrty)
    data['view'] = rts

    print(rts, "//////////////////////")

    system_id_1 = rts[0]['system_details_id']
    system_id_2 = rts[1]['system_details_id']

    print("System Details ID 1:", system_id_1)
    print("System Details ID 2:", system_id_2)

    if 'send' in request.form:
        try:
            file = request.files['file']
            title = request.form['title']

            # Generate and save the file
            path = 'static/' + str(uuid.uuid4()) + file.filename
            file.save(path)

            print(path, "///////////////////////")

            # Generate encryption key and save it
            key = get_random_bytes(32)  # 256-bit key for AES-256
            key_path = f'static/keys/{title}_key.bin'
            os.makedirs('static/keys', exist_ok=True)
            with open(key_path, 'wb') as key_file:
                key_file.write(key)

            # Call the upload_file function with encryption
            dd = upload_file(path, rts, title)

            print(dd, "//////////////////////////+++++++++++++")

            # Extract paths and samples
            pathone = dd[0][2].replace("\\", "\\\\")  # Properly formatted path for part1
            pathtwo = dd[1][2].replace("\\", "\\\\")  # Properly formatted path for part2

            # Extract filenames
            sample1 = dd[0][0]  # Extract filename from the first tuple
            sample2 = dd[1][0]  # Extract filename from the second tuple

            print(pathone, "//////////++++++--------------")
            print(pathtwo, "//////////////++++++++==================")
            print(sample1, "//////////////++++++++ SAMPLE 1")
            print(sample2, "//////////////++++++++ SAMPLE 2")

            from datetime import date
            current_date = date.today()
            print("Current date:", current_date)
            d = current_date.strftime("%Y-%m-%d")

            # Store in blockchain
            with open(compiled_contract_path) as file:
                contract_json = json.load(file)
                contract_abi = contract_json['abi']
            contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
            id = web3.eth.get_block_number()
            
            # Also store the key path in the blockchain
            message = contract.functions.add_upload_file(
                int(id), 
                int(session['user_id']),
                int(system_id_1),
                int(system_id_2),
                title,
                pathone,
                pathtwo,
                sample1,
                sample2,
                d,
                key_path  # Add key path to blockchain storage
            ).transact()
            
            print(message)

            # Clean up the original file
            if os.path.exists(path):
                os.remove(path)

            return "<script>alert('Upload Successfully');window.location='/users_home'</script>"
            
        except Exception as e:
            print("Error during upload:", str(e))
            return "<script>alert('Upload Failed: " + str(e) + "');window.location='/users_home'</script>"

    return render_template('user_upload_share_file.html', data=data)

@users.route('/user_view_share_file')
def user_view_share_file():
    data = {}

    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    blocknumber = web3.eth.get_block_number()
    res = []
    try:
        for i in range(blocknumber, 0, -1):
            a = web3.eth.get_transaction_by_block(i, 0)
            decoded_input = contract.decode_function_input(a['input'])
            print(decoded_input, "///////////////////")
            if str(decoded_input[0]) == "<Function add_upload_file(uint256,uint256,uint256,uint256,string,string,string,string,string,string,string)>":
                if int(decoded_input[1]['user_id']) == int(session['user_id']):
                    res.append(decoded_input[1])
    except Exception as e:
        print("Error retrieving from blockchain:", e)
    data['view'] = res

    print(res, "///////////////////+++++++++")
    
    return render_template('user_view_share_file.html', data=data)

@users.route('/user_retrieve_files')
def user_retrieve_files():
    data = {}
    try:
        upid = request.args['upid']
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json['abi']
        
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        blocknumber = web3.eth.get_block_number()
        res = []
        
        try:
            for i in range(blocknumber, 0, -1):
                a = web3.eth.get_transaction_by_block(i, 0)
                decoded_input = contract.decode_function_input(a['input'])
                print(decoded_input, "///////////////////bbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                if str(decoded_input[0]) == "<Function add_upload_file(uint256,uint256,uint256,uint256,string,string,string,string,string,string,string)>":
                    if int(decoded_input[1]['upload_file_id']) == int(upid):
                        res.append(decoded_input[1])
        except Exception as e:
            print("Error retrieving from blockchain:", e)
        
        data['view'] = res
        
        print(res, "//////////////////////////////0000000000000000000000000000000")
        
        data['system_details_first_id'] = ""
        data['system_details_second_id'] = ""
        
        if res:
            for i in res:
                print(i, "/////////////////////////////////++++++++++++++++++=")
                print(i['system_details_first_id'])
                print(i['system_details_second_id'])
                
                data['view'] = res

                print(data,"//////////////")
                data['system_details_first_id'] = i['system_details_first_id']
                data['system_details_second_id'] = i['system_details_second_id']

        # Retrieve the encryption key path from blockchain data
        key_path = res[0].get('key_path', '')
        if key_path and os.path.exists(key_path):
            with open(key_path, 'rb') as key_file:
                key = key_file.read()
        else:
            raise Exception("Encryption key not found")
        
        # Call retrieve_files with the encryption key
        retrieve_files(res, data['system_details_first_id'], data['system_details_second_id'])
        
        # Clean up the key file after successful retrieval
        # if os.path.exists(key_path):
        #     os.remove(key_path)
        
        return "<script>alert('Retrieve Successfully');window.location='/users_home'</script>"
        
    except Exception as e:
        print("Error during retrieval:", str(e))
        return "<script>alert('Retrieval Failed: " + str(e) + "');window.location='/users_home'</script>"
