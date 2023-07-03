# # ---------------------------------------------- Admin Page -----------------------------------------------

# class Admin:
#     def __init__(self):
#         self.canvas = Canvas(root, width='940', height='500', highlightthickness=0)
#         self.canvas.create_image(0, 0, image=globalImages[7], anchor='nw')
#         self.canvas.pack(side = "top", fill = "both", expand = True)
#         self.mainPage()

#     def mainPage(self):
#         from userpages import AdminAddUser
#         self.btn1 = create_button(root, 'Login', 360, 170, command= lambda: (app.doLogin(), self.selfDestroy()))
#         self.btn3 = create_button(root, 'Add a User', 350, 290, command= lambda: (AdminAddUser(), self.selfDestroy()))

#     def selfDestroy(self):
#         for i in list(self.__dict__.values()):
#             i.destroy()