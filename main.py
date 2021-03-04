def get_quiz():
    filename = 'quiz-questions/1vs1200.txt'
    with open(filename, 'r', encoding='KOI8-R') as file:
        questions = file.read()

    paragraphs = questions.split('Вопрос')[3::]
    questions = []
    answers = []
    for paragraph in paragraphs:
        try:
            question = paragraph.split(
                'Вопрос')[0].split('Ответ')[0].split(':\n')[1]
            questions.append(question)
            answer = paragraph.split('Ответ')[1].split(':')[1].split('\n')[1]
            answers.append(answer)
        except IndexError:
            continue

    quiz = dict(zip(questions, answers))
    return quiz


def main():
    get_quiz()


if __name__ == "__main__":
    main()
