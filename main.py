import telebot
from config import API_KEY, ADMIN_ID
from telebot import types
import storage 
import random

bot = telebot.TeleBot(API_KEY , parse_mode= 'HTML')
owner_id = ADMIN_ID

admin_bottons = ["ثبت محصول", "انبار", "سفارشات"]
user_bottons = ["پروفایل", "محصولات", "سبد خرید"]

flag_add_product = False
flag_panel_products_admin = False
flag_orders = False
flag_panel_products_user = False

edit_product_state = "idle"
add_product_state = "idle"
product = {}
products = []

reply_keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
reply_keyboard_admin.add("ثبت محصول", "انبار", "سفارشات")

reply_keyboard_user = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
reply_keyboard_user.add("پروفایل", "محصولات", "سبد خرید")




inline_keyboard_edit_product = types.InlineKeyboardMarkup()
Edit_name_botton = types.InlineKeyboardButton(text = "ویرایش نام محصول", callback_data= "edit_name_of_product")
Edit_description_botton = types.InlineKeyboardButton(text = "ویرایش توضیحات محصول", callback_data= "edit_description_of_product")
Edit_price_botton = types.InlineKeyboardButton(text = "ویرایش قیمت محصول", callback_data= "edit_price_of_product")
Edit_image_botton = types.InlineKeyboardButton(text = "ویرایش تصویر محصول", callback_data= "edit_image_of_product")
inline_keyboard_edit_product.add(Edit_name_botton, Edit_description_botton, Edit_price_botton, Edit_image_botton)
callback_data_list = ["edit_name_of_product", "edit_description_of_product", "edit_price_of_product", "edit_image_of_product"]

def authentication(admin_id):
    return admin_id == owner_id
    
@bot.message_handler(commands=['admin'] , func= lambda message : authentication(message.from_user.id))
def admin(message):
    bot.send_message(message.chat.id,
                     '<b>به پنل مدیریت فروشگاه خوش آمدید.</b>\n'
'از طریق پنل زیر می‌توانید محصولات و سفارشات فروشگاه را مدیریت کنید'
                     ,reply_markup = reply_keyboard_admin)

@bot.message_handler(func= lambda message : authentication(message.from_user.id) and message.text in admin_bottons)
def admin_panel(message):
    global flag_add_product
    global flag_orders
    global flag_panel_products_admin
    if message.text == "ثبت محصول":
        flag_add_product = True
        add_product(message)
    elif message.text == "سفارشات":
        flag_orders = True
        #show_orders(message)
    elif message.text == "انبار":
        flag_panel_products_admin = True
        show_panel_products_admin(message)


@bot.message_handler(func = lambda message : message.text in user_bottons)
def user_panel(message):
    global flag_panel_products_user
    if message.text == "پروفایل":
        flag_profile = True
        #show_profile(message)
    elif message.text == "محصولات":
        flag_panel_products_user = True
        print(flag_panel_products_user)
        show_user_panel_products(message) 
    elif message.text == "سبد خرید":
        flag_shopping_basket = True
        #show_shopping_basket(message)







@bot.message_handler(func= lambda message : authentication(message.from_user.id) and flag_add_product, content_types=['text', 'photo'])
def add_product(message):
    global add_product_state
    global product
    global flag_add_product
    if message.text == "ثبت محصول" and add_product_state == "idle" :
        bot.send_message(message.chat.id, 'نام محصول خود را وارد کنید.')
        add_product_state = "waiting_for_name"
        product["id"] = random.randint(0,100)

    elif add_product_state == "waiting_for_name" :
        product["name"] = message.text
        bot.send_message(message.chat.id, 'توضیحات محصول را وارد کنید.')
        add_product_state = "waiting_for_description"

    elif add_product_state == "waiting_for_description" :
        product["description"] = message.text
        bot.send_message(message.chat.id, 'قیمت محصول را وارد کنید. ')
        add_product_state = "waiting_for_price"

    elif add_product_state == "waiting_for_price" :
        product["price"] = message.text
        bot.send_message(message.chat.id, 'عکس محصول را ارسال کنید.')
        add_product_state = "waiting_for_image"

    elif add_product_state == "waiting_for_image" :
        product["image"] = message.photo[-1].file_id
        bot.send_message(message.chat.id, 'فرآیند ثبت محصول پایان یافت.')
        add_product_state = "idle"
        storage.save_products(product)
        flag_add_product = False

        print(product)
        
        
@bot.message_handler(func = lambda _ : flag_panel_products_user)
def show_user_panel_products(message):
    global flag_panel_products_user
    product = storage.load_products()
    print(product)
    caption = (
            f"<b>{product[0]['name']}</b>\n"
            f"{product[0]['description']}\n"
            f"Price: {product[0]['price']}"
        )
    bot.send_photo(message.chat.id, product[0]['image'], caption= caption, parse_mode= "HTML")
    flag_panel_products_user = False



def show_panel_products_admin(message):
    global products
    global flag_panel_products_admin
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
    flag_panel_products_admin = True
    


@bot.message_handler(func = lambda message : flag_panel_products_admin and authentication(message.from_user.id) and any(message.text == product["name"] for product in products))
def edit_product(message):
    global flag_panel_products_admin
    global product
    product = next(
    product
    for product in products
    if product["name"] == message.text
)
    caption = (
    f"<b>{product['name']}</b>\n"
    f"{product['description']}\n"
    f"Price: {product['price']}"
)
    bot.send_photo(message.chat.id, product['image'], caption= caption, parse_mode= "HTML", reply_markup= inline_keyboard_edit_product)
    flag_panel_products_admin = False

            

@bot.callback_query_handler(func= lambda call : call.data in  callback_data_list)
def edit_product_details(call):
        global edit_product_state
        match call.data:
            case "edit_name_of_product":
                bot.send_message(call.message.chat.id, "نام جدید محصول:")
                edit_product_state = "edit_name_of_product"
            case "edit_description_of_product":
                bot.send_message(call.message.chat.id, "توضیحات جدید محصول:")
                edit_product_state = "edit_description_of_product"
            case "edit_price_of_product":
                bot.send_message(call.message.chat.id, "قیمت جدید محصول:")
                edit_product_state = "edit_price_of_product"
            case "edit_image_of_product":
                bot.send_message(call.message.chat.id, "تصویر جدید محصول:")
                edit_product_state = "edit_image_of_product"

@bot.message_handler(func= lambda message : authentication(message.from_user.id) and edit_product_state == "edit_name_of_product")
def edit_name_of_product(message):
    global edit_product_state
    product["name"] = message.text
    storage.edit_product(product,"name")
    edit_product_state = "idle"

@bot.message_handler(func = lambda message : authentication(message.from_user.id) and edit_product_state == "edit_description_of_product")
def edit_description_product(message):
    global edit_product_state
    product["description"] = message.text
    storage.edit_product(product, "description")
    edit_product_state = "idle"

@bot.message_handler(func = lambda message : authentication(message.from_user.id) and edit_product_state == "edit_price_of_product")
def edit_price_of_product(message):
    global edit_product_state
    product["price"] = message.text
    storage.edit_product(product,"price")
    edit_product_state = "idle"

@bot.message_handler(func = lambda message : authentication(message.from_user.id) and edit_product_state == "edit_image_of_product", content_types=['photo'])
def edit_photo_of_product(message) :
    global edit_product_state
    product["image"] = message.photo[-1].file_id
    storage.edit_product(product,"image")
    edit_product_state = "idle"

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                 f"سلام! من دستیار شاپ <b> ماهی </b> هستم، و قراره در فرآیند خرید کمکتون کنم. {message.from_user.id}",
                 reply_markup = reply_keyboard_user)    
  

    
bot.infinity_polling()
