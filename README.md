# django-challenge


The volleyball Federation decided to use an online selling platform for the next season, and our company has been chosen for implementing that.

# Requirements

Our system should have REST APIs for the following tasks:

- User signup and login
- Adding a new stadium
- Defining matches
- Defining the place of seats for each match
- Buying seats of a match (There is no need for using a payment gateway)

# Implementation details

We don't need a GUI for this system. You can use the Django admin.
Try to write your code as **reusable** and **readable** as possible. Also, don't forget to **document your code** and clear the reasons for all your decisions in the code.
Using API documentation tools is a plus.
Don't forget that many people trying to buy tickets for a match. So try to implement your code in a way that could handle the load. If your solution is not sample enough for implementing fast, you can just describe it in your documents.

Please fork this repository and add your code to that. Don't forget that your commits are so important. So be sure that you're committing your code often with a proper commit message.


# Apps
- این پروژه جنگویی شامل 4 اپ هست که هرکدام توضیح داده شده اند
- در همه اپ ها به طور کامل برای همه چیز تست نوشته شده است (urls, models, views, serializers) (حدود 2 هزار خط کد)
- پروژه داکرایز شده است
- برای همه view ها، permissions مناسب در نظر گرفته شده است
- API documentation tools used

# Note 

لازم به ذکر است هر 10 دقیقه باید صندلی هایی که رزرو شده ولی پرداخت نشده اند، از حالت رزرو شده در بیایند که
با استفاده از Celery Beat  می تواند انجام شود
البته این مورد پیاده سازی نشده ولی یک نیاز ضروری هست.
دلیل استفاده از Celery Beat :
ما می توانیم بدون استفاده از آن و با چک کردن صندلی در هنگام رزرو شدن که آیا زمان رزروش بیشتر از 10 دقیقه است و پرداختی داشته است یا خیر، این موضوع را بررسی کنیم
ولی این کار باعث افزایش بار دیتابیس شده و پیشنهاد نمی شود

- چون بار پردازشی query ها سنگین خواهد شد

# Note 2

- کاربر  حداقل یک صندلی و حداکثر 10 صندلی می تواند رزرو کند
- بعد از پرداخت، صندلی هایی که کاربر رزرو کرده اپدیت می شوند به is_piad=True
- query ها بهینه طراحی شده اند یعنی در جایی که لازم بوده از متدهای bulk استفاده شده است

# Note 3

- استفاده از مواردی از قبیل throttling, versioning صرف نظر شده است
- CORS  پیاده سازی نشده است
- فایل های مختلفی برای settings  در نظر گرفته شده برای حالات مختلف مثل dev, prod

# 1 - App accounts

- مدل کاربران به طور کامل و از ابتدا با همه مخلفات طراحی شده است (UserModel)
- JWT used for authentication
- There are 4 endpoints : 

    - sign up
    - sign in
    - refresh token
    - verify token

- لازم به ذکر است موارد مربوط به توکن، در حالت پیش فرض قرار دارند و تغییر داده نشده اند
    - مثل ACCESS_TOKEN_LIFETIME
    - مثل REFRESH_TOKEN_LIFETIME


# 2 - App stadium

- There is 1 endpoint
    - Add a new stadium

- This app includes two models :

    - StadiumModel is for maintaining information related to a stadium.
    - SeatModel is for seats which are related to a stadium.

نکات بسیار مهم :

- از قسمت مدیریت باید برای استادیوم مورد نظر صندلی اضافه کنید
- کدهای مربوط به هر صندلی برای هر استادیوم منحصر به فرد هستند (شماره صندلی)
-  هر استادیوم می تواند صندلی هایی داشته باشد که طبق نظر فدراسیون می توانند فروخته شوند یا نه !


# 3 - App Team

از قسمت مدیریت باید تیم هایی اضافه شود


# 4 - App Match

- There are 4 endpoints :

    - Defining a match
    - اضافه کردن یک صندلی با قیمت مشخص از صندلی های استادیومی که مربوط به آن مسابقه هستند به صندلی های فروشی
    - اضافه کردن چند صندلی با قیمت مشخص از صندلی های استادیومی که مربوط به آن مسابقه هستند به صندلی های فروشی
    - رزرو کردن صندلی های یک مسابقه برای خرید قطعی به مدت 10 دقیقه که کاربر فرصت پرداخت داشته باشد

- This app includes two models : Match, MatchSeatInfo

    - MatchModel is for maintaining information related to every match
    - MatchSeatInfo is for maintaining information related to every seat

- There are 4 serializers
    - MatchSerializer ( موارد زیر چک می شوند )
        - دو تیم انتخابی یکسان نباشند
        - در یک استادیوم و یک ساعت مشخص، دو بازی ثبت نشود

    - MatchSeatInfoSerializer ( موارد زیر چک می شوند )

        - صندلی انتخابی قبلا به این بازی اختصاص داده نشده باشد
        - صندلی انتخابی بین صندلی های استادیومی باشد که مسابقه قرار است در آن برگزار شود
    
    - ListCreateMatchSeatInfoSerializer ( موارد زیر چک می شوند )

        - صندلی های انتخابی قبلا به این بازی اختصاص داده نشده باشند
        - صندلی های انتخابی بین صندلی های استادیومی باشد که مسابقه قرار است در آن برگزار شود
    
    - ListUpdateMatchSeatInfoSerializer ( موارد زیر چک می شوند )

        - صندلی ها در حالت رزرو شده نباشند
        -  صندلی های انتخابی بین صندلی های استادیومی باشد که مسابقه قرار است در آن برگزار شود
