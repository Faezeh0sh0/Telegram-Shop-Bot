import telebot
from telebot import types
from config import API_KEY, ADMIN_ID
import storage 
import random

bot = telebot.TeleBot(API_KEY , parse_mode= 'HTML')
owner_id = ADMIN_ID

admin_bottons = ["ثبت محصول", "انبار", "سفارشات"]
user_bottons = ["پروفایل", "محصولات", "سبد خرید"]


flag_orders = False
flag_panel_products_user = False
delete_product_flag = False


product = {}
products = []

reply_keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
reply_keyboard_admin.add("ثبت محصول", "انبار", "سفارشات")

reply_keyboard_user = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
reply_keyboard_user.add("پروفایل", "محصولات", "سبد خرید")

reply_keyboard_delete_product = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
reply_keyboard_delete_product.add("بله", "بازگشت")


inline_keyboard_edit_product = types.InlineKeyboardMarkup()
Edit_name_botton = types.InlineKeyboardButton(text = "ویرایش نام محصول", callback_data= "edit_name_of_product")
Edit_description_botton = types.InlineKeyboardButton(text = "ویرایش توضیحات محصول", callback_data= "edit_description_of_product")
Edit_price_botton = types.InlineKeyboardButton(text = "ویرایش قیمت محصول", callback_data= "edit_price_of_product")
Edit_image_botton = types.InlineKeyboardButton(text = "ویرایش تصویر محصول", callback_data= "edit_image_of_product")
delete_product_button = types.InlineKeyboardButton(text = "حذف محصول", callback_data= "delete_product")
inline_keyboard_edit_product.add(Edit_name_botton, Edit_description_botton, Edit_price_botton, Edit_image_botton, delete_product_button)
callback_data_list = ["edit_name_of_product", "edit_description_of_product", "edit_price_of_product", "edit_image_of_product", "delete_product"]

def authentication(admin_id):
    return admin_id == owner_id


user_sessions = {
    ADMIN_ID : {
        "selected_product" : {},
        "role" : "admin",
        "state" : "idle"
    }
}
    
@bot.message_handler(commands=['admin'] , func= lambda message : authentication(message.from_user.id))
def admin(message):
    bot.send_message(message.chat.id,
                     '<b>به پنل مدیریت فروشگاه خوش آمدید.</b>\n'
'از طریق پنل زیر می‌توانید محصولات و سفارشات فروشگاه را مدیریت کنید'
                     ,reply_markup = reply_keyboard_admin)
    user_sessions[message.from_user.id]["state"] = "idle"

@bot.message_handler(func= lambda message : authentication(message.from_user.id) and message.text in admin_bottons)
def admin_panel(message):
    
    #global flag_orders
    if message.text == "ثبت محصول":
        user_sessions[message.from_user.id]["state"] = "add_product"
        add_product(message)
    elif message.text == "سفارشات":
        flag_orders = True
        #show_orders(message)
    elif message.text == "انبار":
        show_panel_products_admin(message)


@bot.message_handler(func = lambda message : message.text in user_bottons)
def user_panel(message):
    global flag_panel_products_user
    if message.text == "پروفایل":
        flag_profile = True
        #show_profile(message)
    elif message.text == "محصولات":
        user_sessions[message.from_user.id]["state"] = "panel_products_user"
        show_user_panel_products(message) 
    elif message.text == "سبد خرید":
        flag_shopping_basket = True
        #show_shopping_basket(message)







@bot.message_handler(func= lambda message : authentication(message.from_user.id) and user_sessions[message.from_user.id]["state"] in ["add_product", "waiting_for_name", "waiting_for_description", "waiting_for_price", "waiting_for_image"],
                      content_types=['text', 'photo'])
def add_product(message):
    
    global product
    if message.text == "ثبت محصول" and user_sessions[message.from_user.id]["state"] == "add_product" :
        bot.send_message(message.chat.id, 'نام محصول خود را وارد کنید.')
        user_sessions[message.from_user.id]["state"] = "waiting_for_name"
        user_sessions[message.from_user.id]["selected_product"]["id"] = random.randint(0,100)

    elif user_sessions[message.from_user.id]["state"] == "waiting_for_name" :
        user_sessions[message.from_user.id]["selected_product"]["name"] = message.text
        bot.send_message(message.chat.id, 'توضیحات محصول را وارد کنید.')
        user_sessions[message.from_user.id]["state"] = "waiting_for_description"

    elif user_sessions[message.from_user.id]["state"] == "waiting_for_description" :
        user_sessions[message.from_user.id]["selected_product"]["description"] = message.text
        bot.send_message(message.chat.id, 'قیمت محصول را وارد کنید. ')
        user_sessions[message.from_user.id]["state"] = "waiting_for_price"

    elif user_sessions[message.from_user.id]["state"] == "waiting_for_price" :
        user_sessions[message.from_user.id]["selected_product"]["price"] = message.text
        bot.send_message(message.chat.id, 'عکس محصول را ارسال کنید.')
        user_sessions[message.from_user.id]["state"] = "waiting_for_image"

    elif user_sessions[message.from_user.id]["state"] == "waiting_for_image" :
        user_sessions[message.from_user.id]["selected_product"]["image"] = message.photo[-1].file_id
        bot.send_message(message.chat.id, 'فرآیند ثبت محصول پایان یافت.')
        user_sessions[message.from_user.id]["state"] = "idle"
        storage.save_products(user_sessions[message.from_user.id]["selected_product"])
        

        print(user_sessions[message.from_user.id]["selected_product"])
        
        
@bot.message_handler(func = lambda message : user_sessions[message.from_user.id]["state"] == "panel_products_user")
def show_user_panel_products(message):
    products = storage.load_products()
    print(products)
    for product in products:
        caption = (
            f"<b>{product['name']}</b>\n"
            f"{product['description']}\n"
            f"Price: {product['price']}"
        )
        bot.send_photo(message.chat.id, product['image'], caption= caption, parse_mode= "HTML")
    user_sessions[message.from_user.id]["state"] = "idle"



def show_panel_products_admin(message):
    global products
    products = storage.load_products()
    reply_keyboard_products = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    for product in products:

        reply_keyboard_products.add( 
            product["name"]
        )
        print(product['name'])
    
    bot.send_message(message.chat.id, "موجودی انبار قابل مشاهده است.", reply_markup= reply_keyboard_products)
    user_sessions[message.from_user.id]["state"] = "panel_products_admin"
    


@bot.message_handler(func = lambda message : user_sessions[message.from_user.id]["state"] == "panel_products_admin" and authentication(message.from_user.id) and any(message.text == product["name"] for product in products))
def edit_product(message):
    user_sessions[message.from_user.id]["selected_product"] = next(
    product
    for product in products
    if product["name"] == message.text
)
    caption = (
    f"<b>{user_sessions[message.from_user.id]["selected_product"]['name']}</b>\n"
    f"{user_sessions[message.from_user.id]["selected_product"]['description']}\n"
    f"Price: {user_sessions[message.from_user.id]["selected_product"]['price']}"
)
    bot.send_photo(message.chat.id, user_sessions[message.from_user.id]["selected_product"]['image'], caption= caption, parse_mode= "HTML", reply_markup= inline_keyboard_edit_product)
    user_sessions[message.from_user.id]["state"] = "idle"
    #check kon khat bala ro

            

@bot.callback_query_handler(func= lambda call : call.data in  callback_data_list)
def edit_product_details(call):
        match call.data:
            case "edit_name_of_product":
                bot.send_message(call.message.chat.id, "نام جدید محصول:")
                user_sessions[call.from_user.id]["state"] = "edit_name_of_product"
            case "edit_description_of_product":
                bot.send_message(call.message.chat.id, "توضیحات جدید محصول:")
                user_sessions[call.from_user.id]["state"] = "edit_description_of_product"
            case "edit_price_of_product":
                bot.send_message(call.message.chat.id, "قیمت جدید محصول:")
                user_sessions[call.from_user.id]["state"] = "edit_price_of_product"
            case "edit_image_of_product":
                bot.send_message(call.message.chat.id, "تصویر جدید محصول:")
                user_sessions[call.from_user.id]["state"] = "edit_image_of_product"
            case "delete_product" :
                bot.send_message(call.message.chat.id, "آیا از حذف محصول اطمینان دارید؟", reply_markup= reply_keyboard_delete_product)
                user_sessions[call.from_user.id]["state"] = "delete_product"

@bot.message_handler(func= lambda message : authentication(message.from_user.id) and user_sessions[message.from_user.id]["state"] == "edit_name_of_product")
def edit_name_of_product(message):
    user_sessions[message.from_user.id]["selected_product"]["name"] = message.text
    storage.edit_product(user_sessions[message.from_user.id]["selected_product"],"name")
    user_sessions[message.from_user.id]["state"] = "idle"
    bot.send_message(message.chat.id, "ویرایش با موفقیت اعمال شد.")

@bot.message_handler(func = lambda message : authentication(message.from_user.id) and user_sessions[message.from_user.id]["state"] == "edit_description_of_product")
def edit_description_product(message):
    user_sessions[message.from_user.id]["selected_product"]["description"] = message.text
    storage.edit_product(user_sessions[message.from_user.id]["selected_product"], "description")
    user_sessions[message.from_user.id]["state"] = "idle"
    bot.send_message(message.chat.id, "ویرایش با موفقیت اعمال شد.")

@bot.message_handler(func = lambda message : authentication(message.from_user.id) and user_sessions[message.from_user.id]["state"] == "edit_price_of_product")
def edit_price_of_product(message):
    user_sessions[message.from_user.id]["selected_product"]["price"] = message.text
    storage.edit_product(user_sessions[message.from_user.id]["selected_product"],"price")
    user_sessions[message.from_user.id]["state"] = "idle"
    bot.send_message(message.chat.id, "ویرایش با موفقیت اعمال شد.")

@bot.message_handler(func = lambda message : authentication(message.from_user.id) and user_sessions[message.from_user.id]["state"] == "edit_image_of_product", content_types=['photo'])
def edit_photo_of_product(message) :
    user_sessions[message.from_user.id]["selected_product"]["image"] = message.photo[-1].file_id
    storage.edit_product(user_sessions[message.from_user.id]["selected_product"],"image")
    user_sessions[message.from_user.id]["state"] = "idle"
    bot.send_message(message.chat.id, "ویرایش با موفقیت اعمال شد.")

@bot.message_handler(func= lambda message : authentication(message.from_user.id) and user_sessions[message.from_user.id]["state"] == "delete_product" and message.text in ["بله", "بازگشت"])
def delete_the_product(message) :
    if message.text == "بله":
        storage.delete_product(user_sessions[message.from_user.id]["selected_product"]["id"])
        user_sessions[message.from_user.id]["state"] = "idle"
    elif message.text == "بازگشت":
        user_sessions[message.from_user.id]["state"] = "idle"
        show_panel_products_admin(message)
    else:
        bot.send_message(message.chat.id, "دستور نامعتبر است.")


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                 f"سلام! من دستیار شاپ <b> ماهی </b> هستم، و قراره در فرآیند خرید کمکتون کنم. {message.from_user.id}",
                 reply_markup = reply_keyboard_user)    
  

    
bot.infinity_polling()
