import telebot
from config import API_KEY, ADMIN_ID
from telebot import types
import storage 
bot = telebot.TeleBot(API_KEY , parse_mode= 'HTML')
owner_id = ADMIN_ID
admin_bottons = ["ثبت محصول", "محصولات", "سفارشات"]
user_bottons = ["پروفایل", "محصولات", "سبد خرید"]
flag_add_product = False
flag_panel_products_admin = False
flag_orders = False
add_product_state = "idle"
product = {}
reply_keyboard_admin = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
reply_keyboard_admin.add("ثبت محصول", "محصولات", "سفارشات")

reply_keyboard_user = types.ReplyKeyboardMarkup(resize_keyboard= True, one_time_keyboard= True)
reply_keyboard_user.add("پروفایل", "محصولات", "سبد خرید")


@bot.message_handler(commands=['admin'] , func= lambda message : message.from_user.id == owner_id)
def admin(message):
    bot.send_message(message.chat.id,
                     '<b>به پنل مدیریت فروشگاه خوش آمدید.</b>\n'
'از طریق پنل زیر می‌توانید محصولات و سفارشات فروشگاه را مدیریت کنید'
                     ,reply_markup = reply_keyboard_admin)

@bot.message_handler(func= lambda message : message.from_user.id == owner_id and message.text in admin_bottons)
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
    elif message.text == "محصولات":
        flag_panel_products_admin = True
        #show_panel_products(message)


@bot.message_handler(func = lambda message : message.text in user_bottons)
def user_panel(message):
    if message.text == "پروفایل":
        flag_profile = True
        #show_profile(message)
    elif message.text == "محصولات":
        flag_panel_products_user = True
        #show_panel_products(message) it's the same with the name of this button in admin panel 
    elif message.text == "سبد خرید":
        flag_shopping_basket = True
        #show_shopping_basket(message)



@bot.message_handler(func= lambda message : message.from_user.id == owner_id and flag_add_product, content_types=['text', 'photo'])
def add_product(message):
    global add_product_state
    global product
    if message.text == "ثبت محصول" and add_product_state == "idle" :
        bot.send_message(message.chat.id, 'نام محصول خود را وارد کنید.')
        add_product_state = "waiting_for_name"

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
        print(product)
        
        
        

    
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                 f"سلام! من دستیار شاپ <b> ماهی </b> هستم، و قراره در فرآیند خرید کمکتون کنم. {message.from_user.id}",
                 reply_markup = reply_keyboard_user)    
  

    
bot.infinity_polling()
