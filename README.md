
# 웹 개발 새로고침
![입체_웹개발새로고침_766x766_72DPI](https://github.com/sgkim-pub/pyBook/assets/77865135/ee694b2a-26cf-4877-9d57-1bfe59dfda93)

책의 예제 소스 코드들을 찾아보실 수 있습니다.

현재 보고 계시는 마스터 브랜치 외에 책의 각 챕터에 해당하는 브랜치를 브랜치 드롭다운 버튼을 이용해 찾아보실 수 있습니다.

![웹개발새로고침_3장4장_소스코드_찾아보기_버튼표시](https://github.com/sgkim-pub/pyBook/assets/77865135/71e6fe42-7a8e-49ca-a5e2-75b64655ad97)

책의 2장에 해당하는 예제 소스 코드들을 아래 위치에서 찾아보실 수 있습니다.

[2장 전반부 - 웹 프로그램 기본 구조와 작동 원리](https://github.com/sgkim-pub/pyWorld)

[2장 후반부 - HTML, JavaScript](https://github.com/sgkim-pub/html_js)

책에서 백엔드 코드 작성에 사용했던 파이썬과 파이참(PyCharm)을 아래 경로에서 찾으실 수 있습니다. 파이참은 순수 파이썬 개발용 Community Edition을 다운로드하고 이용하시면 됩니다.

파이썬: <https://www.python.org/>

파이참: <https://www.jetbrains.com/ko-kr/pycharm/download/?section=windows>

---

모든 작가가 책에 가능하면 많은 내용을 담아서 드리고 싶을 것입니다. 하지만 웹 프로그램의 작동 원리와 이를 확인하는 실습 코드를 중심으로 핵심적이라고 생각되는 내용들을 중심으로 책을 구성하였습니다.

시간이 흐르면서 최신 기술이 책의 일부 내용과 다르거나 책의 일부 예제들이 매끄럽게 동작하지 않을 수 있습니다. 책에 기재되어 있는 저자 연락처로 내용을 알려주시면 책의 판본을 변경할 기회가 될 때 반영해 보겠습니다.

---

안녕하세요? 아래와 같은 오류로 파이썬 플라스크를 사용하는 예제의 백엔드 코드가 실행되지 않는 경우가 있습니다.

```
...
ImportError: cannot import name 'url_quote' from 'werkzeug.urls' (.../lib/python3.10/site-packages/werkzeug/urls.py)
...
```

Werkzeug는 파이썬 플라스크가 사용하는 라이브러리입니다. 이 Werkzeug의 버전이 플라스크 버전과 맞지 않아서 생기는 문제입니다.

A) 최신 버전의 플라스크를 설치해서 사용하시거나, B) 플라스크 이전 버전과 호환되는 Werkzeug 라이브러리를 재설치하시면 오류를 해결하실 수 있습니다.

A) 최신 버전의 플라스크를 설치해서 사용
```
(venv) $> pip3 install Flask
```

B) 플라스크 이전 버전(예, 2.2.2)과 호환되는 Werkzeug 라이브러리를 재설치
```
(venv) $> pip3 list
...
Flask  2.2.2
... 
Werkzeug	3.0.0
...
(venv) $> pip3 uninstall Werkzeug
(venv) $> pip3 install Werkzeug==2.2.2
(venv) $> pip3 list
... 
Werkzeug	2.2.2
...
```
