from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from Backend.server import client_req_msg, SUCCESS, FAILURE, BUFF_SIZE
import pickle
import datetime
# from Frontend.writepostpage import WritePostPage 
from Frontend.show_friend_list import Show_friend_list
# from Frontend.homepage import HomePage, WritePostPage

class UserWall:
    '''
    Here Posts will be shown
    '''
    def __init__(self, root, client_socket, username, user2):
        
        self.root = root 
        self.username = username
        self.user2 = user2
        self.root.title(user2 + " Home Window")
        self.root.geometry("900x600+0+0")
        self.client_socket = client_socket

        self.ownership_dict = {
            0: "Public",
            1: "Private",
            2: "Strictly Private"
        }

        self.ownership_colors = {
            0:'green',
            1:'orange',
            2:'red'
        }

        self.users = 0

        ###################################### search from registered users ##########################################################################
        
        self.Frame_users=Frame(self.root,bg="gray")
        self.Frame_users.place(x=610,y=10,height=700,width=300)

        self.txt_search=Entry(self.Frame_users,font=("Times New Roman",15),bg="lightgray")  
        self.txt_search.place(x=5,y=10,width=200,height=35)
        search_btn = Button(self.Frame_users,command=self.search_users,cursor="hand2",text="Search Name",bg="gray",fg="white",font=("Times New Roman",15)).place(x=5,y=60) 
        search_all_btn = Button(self.Frame_users,command=self.search_all_users,cursor="hand2",text="All Users",bg="gray",fg="white",font=("Times New Roman",15)).place(x=5,y=200) 
        Logout=Button(self.Frame_users,cursor="hand2",text="LOGOUT",bg="white",fg="#d77337",bd=0,font=("Times New Roman",12), command = self.logout).place(x=100,y=450)
      
        ###############################################################################################################################################




        ################################################### fetch all users post ##########################################################################
        
        Frame_posts=Frame(self.root,bg="white")
        Frame_posts.place(x=10,y=10,height=700,width=600)

        client_req_msg['command'] = "FETCH_USER_POSTS"
        client_req_msg['body'] = self.user2
        client_req = pickle.dumps(client_req_msg) # convers the client req message to bytes
        self.client_socket.send(client_req)

        # Server Response -> [[post], [post], ....]
        server_response = self.client_socket.recv(BUFF_SIZE) # receive from server
        server_response = pickle.loads(server_response, encoding='utf-8') # convert to dictionary

        if server_response['status_line']['status_code'] == SUCCESS:
            print("Posts Fetched!")

            posts = server_response['data']
            
        else:
            print("Fetching users failed!");
            posts = 0
        
        ###############################################################################################################################################
        

        
        
        ################################################### display data ############################################################################
        # i = 1
        scrollbar = tk.Scrollbar(Frame_posts)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        y = 100
        if posts:
            for post in posts:
                username = Label(Frame_posts,text= 'By @' + post[0],font=("Times",10),fg="#d77337",bg="white").place(x=20,y=y)
                published_at = Label(Frame_posts,text= post[3],font=("Times",8),fg="gray",bg="white").place(x=120,y=y)
                ownership = Label(Frame_posts, text=self.ownership_dict[post[4]], font=("Times",8),fg=self.ownership_colors[post[4]],bg="white").place(x=400,y=y)
                title = Label(Frame_posts,text= '*'  +  ' Title :'+ post[1],font=("Times",10, "bold"),fg="#d77337",bg="white").place(x=10,y=y+20)
                content = Label(Frame_posts,text=post[2],font=("Times",10),fg="blue",bg="white").place(x=10,y=y+40)
                
                # Canvas.create_line(10, y+60, 600, y+61)
                y += 100
            # i += 1

        # Post=Button(self.Frame_users,command=self.write_post_page,cursor="hand2",text="Write Post",bg="white",fg="#d77337",font=("Times New Roman",12)).place(x=100,y=400)
        text1 = Label(Frame_posts,text= '@' + self.user2 + ' Posts',font=("Times",20),fg="green",bg="white").place(x=10,y=60)

        welcometext = Label(Frame_posts,text= "Welcome @" + self.username,font=("Times",22),fg="blue",bg="white").place(x=10,y=10)
        ###############################################################################################################################################
        # friend list button
        # My_Friends=Button(Frame_posts,command=self.friends_page,cursor="hand2",text="FRIENDS LIST",bg="white",fg="#d77337",font=("Times New Roman",15)).place(x=400,y=10)
  



    '''
    # Another window of friend list  
    '''
    
    def friends_page(self):    
        
        master4 = Tk()
        # print("Username: ", self.user)

        app4 = Show_friend_list(master4, self.client_socket, self.username)
        # self.root.destroy()
        master4.mainloop()    


    '''
    when 'Search all users' button is clicked
    '''
    def search_all_users(self):
        # Server request - Fetch all users!
        client_req_msg['command'] = "FETCH_USERS"
        client_req = pickle.dumps(client_req_msg) # convers the client req message to bytes
        self.client_socket.send(client_req)

        # Server Response -> [username, username, ....]
        server_response = self.client_socket.recv(BUFF_SIZE) # receive from server
        server_response = pickle.loads(server_response, encoding='utf-8') # convert to dictionary
        
        if server_response['status_line']['status_code'] == SUCCESS:
            print("Users Fetched!")

            users = server_response['data']

        ################################################### display all users ############################################################################
        
            y = 250
            for user in users:
                if user != self.username:
                    username=Label(self.Frame_users,text=user,font=("Impact",10),fg="white",bg="gray").place(x=10,y=y)
                    # visit_btn=Button(self.Frame_users,cursor="hand2",text="Visit",bg="gray",fg="white",bd=0,font=("Times New Roman",10), command = partial(self.visit_user,user)).place(x=60,y=y)
                    y += 30
            
        else:
            print("Fetching users failed!");
            # add message box here!
        
        ###############################################################################################################################################



    '''
    When username in search field is entered
    '''
    def search_users(self):
        # Server request - Fetch all users!
        client_req_msg['command'] = "FETCH_USER"
        client_req_msg['body'] = self.txt_search.get().lower() # get the searched user entry
        print(self.txt_search.get().lower())
        client_req = pickle.dumps(client_req_msg) # convers the client req message to bytes
        self.client_socket.send(client_req)

        # Server Response -> user or user not found!
        server_response = self.client_socket.recv(BUFF_SIZE) # receive from server
        server_response = pickle.loads(server_response, encoding='utf-8') # convert to dictionary
        
        if server_response['status_line']['status_code'] == SUCCESS:
            print("Users Fetched!")
            searched_user = server_response['data']

            ################################################### display searched users ############################################################################
        
            y = 100
            username=Label(self.Frame_users,text=searched_user,font=("Impact",10),fg="white",bg="gray").place(x=10,y=y)
            # add_friend=Button(self.Frame_users,cursor="hand2",text="Add Friend",bg="gray",fg="white",bd=0,font=("Times New Roman",10), command = self.add_friend).place(x=60,y=y)
        
            ###############################################################################################################################################
            
        else:
            print("Fetching user failed!");
            messagebox.showerror("Error","Incorrect username!",parent=self.root)
    
    '''
    Log out
    '''
    def logout(self):
        
         # Server request - log out
        client_req_msg['command'] = "LOG_OUT"
        client_req = pickle.dumps(client_req_msg) # convers the client req message to bytes
        self.client_socket.send(client_req)

    
        server_response = self.client_socket.recv(BUFF_SIZE) # receive from server
        server_response = pickle.loads(server_response, encoding='utf-8') # convert to dictionary
        
        if server_response['status_line']['status_code'] == SUCCESS:
            print("log out")
            self.root.destroy()
         
            
        else:
            print("log out failed!");
            messagebox.showerror("Error","logout failed!",parent=self.root)
    
        
    