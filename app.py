import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="마지막 교실",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 게임 전체를 HTML + CSS + JavaScript로 실행
# =========================================================

game = r"""
<!DOCTYPE html>
<html lang="ko">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 0;

    background:
        radial-gradient(
            circle at center,
            #303030,
            #101010 70%
        );

    color: white;

    font-family:
        Arial,
        "Noto Sans KR",
        sans-serif;

    overflow: hidden;
}

/* =====================================================
   전체 게임
   ===================================================== */

#game-wrapper {

    width: 100%;

    min-height: 100vh;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    padding: 15px;
}

/* =====================================================
   제목
   ===================================================== */

#title {

    color: #e8d49a;

    font-size: 30px;

    font-weight: 900;

    margin-bottom: 8px;

    text-shadow:
        3px 3px #000,
        0 0 10px #d7b866;
}

#subtitle {

    color: #aaa;

    margin-bottom: 12px;

    font-size: 14px;
}

/* =====================================================
   게임 화면
   ===================================================== */

#game {

    position: relative;

    width: 600px;

    max-width: 95vw;

    aspect-ratio: 10 / 7;

    background: #111;

    border: 8px solid #292929;

    box-shadow:
        0 0 0 3px #111,
        0 15px 40px rgba(0,0,0,0.7);

    overflow: hidden;
}

/* =====================================================
   맵
   ===================================================== */

#map {

    position: absolute;

    inset: 0;

    display: grid;

    grid-template-columns:
        repeat(10, 1fr);

    grid-template-rows:
        repeat(7, 1fr);
}

/* =====================================================
   타일
   ===================================================== */

.tile {

    display: flex;

    justify-content: center;

    align-items: center;

    font-size: clamp(18px, 4vw, 32px);

    user-select: none;
}

.floor {

    background:
        repeating-linear-gradient(
            45deg,
            #65594d 0px,
            #65594d 18px,
            #5a4f45 18px,
            #5a4f45 36px
        );

    border:
        1px solid rgba(0,0,0,0.18);
}

.wall {

    background:
        repeating-linear-gradient(
            135deg,
            #242424 0px,
            #242424 12px,
            #303030 12px,
            #303030 24px
        );

    border:
        2px solid #111;
}

/* =====================================================
   오브젝트
   ===================================================== */

.object {

    position: absolute;

    width: 10%;

    height: 14.2857%;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: clamp(20px, 5vw, 38px);

    transition:
        left 0.08s linear,
        top 0.08s linear;

    z-index: 10;

    user-select: none;
}

/* =====================================================
   플레이어
   ===================================================== */

#player {

    filter:
        drop-shadow(
            3px 4px 2px
            rgba(0,0,0,0.8)
        );

    z-index: 30;
}

/* =====================================================
   대화창
   ===================================================== */

#dialogue {

    width: 600px;

    max-width: 95vw;

    min-height: 70px;

    margin-top: 10px;

    padding: 12px 16px;

    background: #111;

    border: 3px solid #666;

    border-radius: 5px;

    box-shadow:
        0 5px 15px
        rgba(0,0,0,0.5);

    font-size: 14px;

    line-height: 1.6;
}

#speaker {

    color: #e6c45d;

    font-weight: bold;

    margin-bottom: 3px;
}

/* =====================================================
   상태창
   ===================================================== */

#status {

    width: 600px;

    max-width: 95vw;

    display: flex;

    justify-content: space-between;

    padding: 8px 12px;

    margin-top: 8px;

    background: #151515;

    border: 2px solid #444;

    border-radius: 5px;

    font-size: 13px;
}

/* =====================================================
   조작 설명
   ===================================================== */

#controls {

    width: 600px;

    max-width: 95vw;

    text-align: center;

    color: #aaa;

    margin-top: 8px;

    font-size: 13px;
}

/* =====================================================
   모바일 방향키
   ===================================================== */

#mobile-controls {

    display: none;

    margin-top: 10px;

    grid-template-columns:
        repeat(3, 55px);

    grid-template-rows:
        repeat(2, 50px);

    gap: 5px;
}

.control-button {

    background: #292929;

    color: white;

    border: 2px solid #555;

    border-radius: 7px;

    font-size: 22px;

    cursor: pointer;

    touch-action: manipulation;
}

.control-button:active {

    background: #555;
}

.up {
    grid-column: 2;
}

.left {
    grid-column: 1;
}

.down {
    grid-column: 2;
}

.right {
    grid-column: 3;
}

/* =====================================================
   엔딩
   ===================================================== */

#ending {

    position: absolute;

    inset: 0;

    z-index: 100;

    display: none;

    flex-direction: column;

    align-items: center;

    justify-content: center;

    text-align: center;

    background:
        rgba(0,0,0,0.94);

    padding: 30px;
}

#ending h1 {

    color: #f3d36c;

    font-size: 40px;

    margin-bottom: 10px;
}

#ending p {

    line-height: 1.8;

    color: #ddd;
}

#restart {

    margin-top: 15px;

    padding: 12px 25px;

    background: #343434;

    color: white;

    border: 2px solid #777;

    border-radius: 6px;

    cursor: pointer;

    font-weight: bold;
}

#restart:hover {

    background: #4a4a4a;
}


/* =====================================================
   모바일
   ===================================================== */

@media (max-width: 700px) {

    #mobile-controls {

        display: grid;
    }

    #controls {

        display: none;
    }

    #title {

        font-size: 25px;
    }

}

</style>

</head>


<body>


<div id="game-wrapper">


<div id="title">
🏫 마지막 교실
</div>


<div id="subtitle">
Chapter 1 — 잠긴 교실
</div>


<!-- ===================================================
     게임 화면
     =================================================== -->

<div id="game">


<div id="map"></div>


<!-- 플레이어 -->

<div
    id="player"
    class="object"
>
🧍
</div>


<!-- 상자 -->

<div
    id="box"
    class="object"
>
📦
</div>


<!-- 열쇠 -->

<div
    id="key"
    class="object"
>
🗝️
</div>


<!-- 문 -->

<div
    id="door"
    class="object"
>
🚪
</div>


<!-- 엔딩 -->

<div id="ending">

<h1>
🎉 탈출 성공!
</h1>

<p>
철컥...
</p>

<p>
잠겨 있던 교실 문이 열렸다.
</p>

<p>
당신은 무사히 교실에서 탈출했다.
</p>

<p>
<b>THE END</b>
</p>

<button id="restart">
🔄 다시 플레이
</button>

</div>


</div>


<!-- ===================================================
     대화창
     =================================================== -->

<div id="dialogue">

<div id="speaker">
🧍 나
</div>

<div id="message">

WASD 또는 방향키를 사용해서 이동하세요.
<br>
📦 상자를 밀어서 🗝️ 열쇠를 얻고 🚪 문으로 가세요.

</div>

</div>


<!-- ===================================================
     상태창
     =================================================== -->

<div id="status">

<span id="key-status">
🔒 열쇠 없음
</span>

<span>
👣 이동:
<span id="moves">0</span>
</span>

</div>


<!-- ===================================================
     키보드 안내
     =================================================== -->

<div id="controls">

⌨️ 방향키 또는 W A S D 로 이동

</div>


<!-- ===================================================
     모바일 조작
     =================================================== -->

<div id="mobile-controls">

<button
    class="control-button up"
    data-dir="up"
>
⬆️
</button>

<button
    class="control-button left"
    data-dir="left"
>
⬅️
</button>

<button
    class="control-button down"
    data-dir="down"
>
⬇️
</button>

<button
    class="control-button right"
    data-dir="right"
>
➡️
</button>

</div>


</div>


<script>

/* =====================================================
   맵

   # = 벽
   . = 바닥

   맵 크기:

   10 x 7
   ===================================================== */

const MAP = [

    "##########",

    "#........#",

    "#.###....#",

    "#........#",

    "#....###.#",

    "#........#",

    "##########"

];


/* =====================================================
   게임 상태
   ===================================================== */

let player = {

    x: 1,

    y: 1

};


let box = {

    x: 3,

    y: 3

};


let key = {

    x: 7,

    y: 1,

    collected: false

};


let door = {

    x: 8,

    y: 1

};


let moves = 0;

let hasKey = false;

let gameClear = false;


/* =====================================================
   HTML 요소
   ===================================================== */

const mapElement =
    document.getElementById("map");

const playerElement =
    document.getElementById("player");

const boxElement =
    document.getElementById("box");

const keyElement =
    document.getElementById("key");

const doorElement =
    document.getElementById("door");

const messageElement =
    document.getElementById("message");

const keyStatus =
    document.getElementById("key-status");

const movesElement =
    document.getElementById("moves");

const endingElement =
    document.getElementById("ending");

const restartButton =
    document.getElementById("restart");


/* =====================================================
   맵 생성
   ===================================================== */

function createMap() {

    mapElement.innerHTML = "";

    for (
        let y = 0;
        y < MAP.length;
        y++
    ) {

        for (
            let x = 0;
            x < MAP[y].length;
            x++
        ) {

            const tile =
                document.createElement("div");

            tile.classList.add("tile");

            if (MAP[y][x] === "#") {

                tile.classList.add("wall");

            } else {

                tile.classList.add("floor");

            }

            mapElement.appendChild(tile);

        }

    }

}


/* =====================================================
   오브젝트 위치 계산
   ===================================================== */

function setPosition(element, x, y) {

    element.style.left =
        (x * 10) + "%";

    element.style.top =
        (y * 14.2857) + "%";

}


/* =====================================================
   화면 업데이트
   ===================================================== */

function render() {

    setPosition(
        playerElement,
        player.x,
        player.y
    );


    setPosition(
        boxElement,
        box.x,
        box.y
    );


    setPosition(
        doorElement,
        door.x,
        door.y
    );


    if (!key.collected) {

        setPosition(
            keyElement,
            key.x,
            key.y
        );

        keyElement.style.display =
            "flex";

    } else {

        keyElement.style.display =
            "none";

    }


    movesElement.textContent =
        moves;


    if (hasKey) {

        keyStatus.textContent =
            "🗝️ 열쇠 있음";

    } else {

        keyStatus.textContent =
            "🔒 열쇠 없음";

    }

}


/* =====================================================
   타일이 이동 가능한지 확인
   ===================================================== */

function isWall(x, y) {

    if (
        y < 0 ||
        y >= MAP.length ||
        x < 0 ||
        x >= MAP[0].length
    ) {

        return true;

    }

    return MAP[y][x] === "#";

}


/* =====================================================
   대화 메시지
   ===================================================== */

function message(text) {

    messageElement.innerHTML =
        text;

}


/* =====================================================
   플레이어 이동
   ===================================================== */

function move(dx, dy) {

    if (gameClear) {

        return;

    }


    const nextX =
        player.x + dx;

    const nextY =
        player.y + dy;


    /* 벽 */

    if (
        isWall(
            nextX,
            nextY
        )
    ) {

        message(
            "🧱 벽이다. 더 이상 갈 수 없다."
        );

        return;

    }


    /* =================================================
       상자
       ================================================= */

    if (
        nextX === box.x &&
        nextY === box.y
    ) {

        const boxNextX =
            box.x + dx;

        const boxNextY =
            box.y + dy;


        /* 상자 뒤가 벽 */

        if (
            isWall(
                boxNextX,
                boxNextY
            )
        ) {

            message(
                "📦 상자가 벽에 막혀 있다."
            );

            return;

        }


        /* 상자 뒤에 문 */

        if (
            boxNextX === door.x &&
            boxNextY === door.y
        ) {

            message(
                "📦 문 앞이라 상자를 더 밀 수 없다."
            );

            return;

        }


        /* 상자 이동 */

        box.x =
            boxNextX;

        box.y =
            boxNextY;


        player.x =
            nextX;

        player.y =
            nextY;


        moves++;

        message(
            "📦 상자를 밀었다."
        );

        checkItems();

        render();

        return;

    }


    /* =================================================
       문
       ================================================= */

    if (
        nextX === door.x &&
        nextY === door.y
    ) {

        if (hasKey) {

            player.x =
                nextX;

            player.y =
                nextY;

            moves++;

            render();

            win();

            return;

        } else {

            message(
                "🚪 문이 잠겨 있다. 🗝️ 열쇠가 필요하다."
            );

            return;

        }

    }


    /* =================================================
       일반 이동
       ================================================= */

    player.x =
        nextX;

    player.y =
        nextY;

    moves++;


    checkItems();

    render();

}


/* =====================================================
   아이템 확인
   ===================================================== */

function checkItems() {

    /* 열쇠 */

    if (
        !key.collected &&
        player.x === key.x &&
        player.y === key.y
    ) {

        key.collected = true;

        hasKey = true;

        message(
            "🗝️ 열쇠를 얻었다! 🚪 문으로 돌아가자."
        );

    }


    /* 상자를 열쇠 위에 밀어놓는 경우 */

    if (
        !key.collected &&
        box.x === key.x &&
        box.y === key.y
    ) {

        key.collected = true;

        hasKey = true;

        message(
            "📦 상자를 옮기자 아래에서 🗝️ 열쇠가 나타났다!"
        );

    }

}


/* =====================================================
   게임 성공
   ===================================================== */

function win() {

    gameClear = true;

    endingElement.style.display =
        "flex";

}


/* =====================================================
   다시 시작
   ===================================================== */

function restart() {

    player = {

        x: 1,

        y: 1

    };


    box = {

        x: 3,

        y: 3

    };


    key = {

        x: 7,

        y: 1,

        collected: false

    };


    moves = 0;

    hasKey = false;

    gameClear = false;


    endingElement.style.display =
        "none";


    message(
        "WASD 또는 방향키를 사용해서 이동하세요.<br>" +
        "📦 상자를 밀어서 🗝️ 열쇠를 얻고 🚪 문으로 가세요."
    );


    render();

}


/* =====================================================
   키보드 입력
   ===================================================== */

document.addEventListener(
    "keydown",
    function(event) {

        const keyPressed =
            event.key.toLowerCase();


        if (
            [
                "arrowup",
                "arrowdown",
                "arrowleft",
                "arrowright",
                "w",
                "a",
                "s",
                "d"
            ].includes(keyPressed)
        ) {

            event.preventDefault();

        }


        if (
            keyPressed === "arrowup" ||
            keyPressed === "w"
        ) {

            move(0, -1);

        }


        else if (
            keyPressed === "arrowdown" ||
            keyPressed === "s"
        ) {

            move(0, 1);

        }


        else if (
            keyPressed === "arrowleft" ||
            keyPressed === "a"
        ) {

            move(-1, 0);

        }


        else if (
            keyPressed === "arrowright" ||
            keyPressed === "d"
        ) {

            move(1, 0);

        }

    }
);


/* =====================================================
   모바일 버튼
   ===================================================== */

document
    .querySelectorAll(".control-button")
    .forEach(
        button => {

            button.addEventListener(
                "click",
                function() {

                    const direction =
                        this.dataset.dir;


                    if (
                        direction === "up"
                    ) {

                        move(0, -1);

                    }

                    else if (
                        direction === "down"
                    ) {

                        move(0, 1);

                    }

                    else if (
                        direction === "left"
                    ) {

                        move(-1, 0);

                    }

                    else if (
                        direction === "right"
                    ) {

                        move(1, 0);

                    }

                }
            );

        }
    );


/* =====================================================
   다시 시작 버튼
   ===================================================== */

restartButton.addEventListener(
    "click",
    restart
);


/* =====================================================
   게임 시작
   ===================================================== */

createMap();

render();

</script>

</body>

</html>
"""


# =========================================================
# Streamlit에 게임 삽입
# =========================================================

components.html(
    game,
    height=850,
    scrolling=False
)
:::
---

# 4. 완성된 GitHub 구조

GitHub에서 다음처럼 보이면 됩니다.

```text
📁 last-classroom
│
├── 📄 app.py
│
└── 📄 requirements.txt
