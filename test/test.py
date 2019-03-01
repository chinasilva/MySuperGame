
from aitext import Ai

def main():
    # issue='《瓦尔登湖》、《霍乱时期的爱情》、《远大前程》,哪部作品的作'
    # answer=['《瓦尔登湖》','《霍乱时期的爱情》','《远大前程》']
    # issue='同一年中,下列哪个节气最早?'
    # answer=['冬至','立冬','小雪']
    issue='影视领域常用的“杀青”一词,最初是哪项活动的一个程序?'
    # issue=''
    answer=['制竹简','制茶','造纸']
    ai = Ai(issue, answer)
    ai.search()


if __name__ == '__main__':
    main()