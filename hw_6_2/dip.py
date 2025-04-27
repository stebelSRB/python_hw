
# --------------------------- Homework_6.2  ------------------------------------

'''

Виконав: Роман Стебельський

Homework_6.2 Принцип інверсії залежностей

'''


# Dependency Inversion

class NewsPaper:

    @staticmethod
    def publish(news: str) -> None:
        print(f"{news} published today")

class Reporter(NewsPaper):

    @staticmethod
    def publish(news: str) -> None:
        NewsPaper.publish(news=news)


Reporter.publish("News Paper")



'''


'''