## Twitter Clone with Django Rest Framework

This project allows:
- Register Users
- Login Users
- Follow another users
- Unfollow another Users
- Post tweets
- Like Tweets
- Unlike Tweets

All API request after login require JWT access token, you can get this token in the next end-point:
```shell
http://localhost:8000/api/auth/token/
```

### Different ways to run this Project:
- docker-compose
- Regular django project

#### Docker
Execute the next command in the source folder:
```shell
docker-compose up --build
```

#### Regular django project
Inside directory `twitter-clone-drf` execute:
```shell
python manage.py runserver
```

You can see the project documentation in: 
```shell
http://localhost:8000/swagger/
```
If you want to see this project in production environment, you can visit the next url: 
www.jcalarcon.me/twitter-clone/swagger

## Code Coverage
This project has a code coverage of 89%

To run code coverage, in `twitter-clone-drf/` directory you can execute:
```shell
coverage run manage.py test
```

After that you can obtain the report in different formats, the most used is HTML format, to obtain that report
you can execute:
```shell
coverage html
```

## Author

👤 **Jean Carlos Alarcón**

[![Twitter Follow](https://img.shields.io/twitter/follow/jcalarcon98?color=1DA1F2&label=Follow%20me%20on%20Twitter%21&logo=twitter&style=for-the-badge)](https://twitter.com/jcalarcon98)

* Twitter: [@jcalarcon98](https://twitter.com/jcalarcon98)
* Github: [@jcalarcon98](https://github.com/jcalarcon98)
* LinkedIn: [@jcalarcon98](https://linkedin.com/in/jcalarcon98)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2021 [Jean Carlos Alarcón](https://github.com/jcalarcon98).

This project is under [MIT](https://opensource.org/licenses/MIT) licensed.

***