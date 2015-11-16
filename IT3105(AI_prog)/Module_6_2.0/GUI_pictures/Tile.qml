import QtQuick 1.0

Image {
    id: flipable
    property int angle: 0

    width: 40;  height: 40
    transform: Rotation { origin.x: width/2; origin.y: height/2; axis.x: 1; axis.z: 0; angle: flipable.angle }

    property int statusInt: modelData.status
    
    source: {
        if (statusInt === 0) {
            "pics/2048/0.png" 
        } 
        else if (statusInt === 2) { 
             "pics/2048/2.png"
        } 
        else if (statusInt === 4){
            "pics/2048/4.png"
        }
        else if (statusInt === 8) {
            "pics/2048/8.png"
        } 
        else if (statusInt === 16) {
             "pics/2048/16.png"
        } 
        else if (statusInt === 32) {
             "pics/2048/32.png"
        } 
        else if (statusInt === 64) {
             "pics/2048/64.png"
        }
        else if (statusInt === 128) {
             "pics/2048/128.png"
        }
        else if (statusInt === 256) {
             "pics/2048/256.png"
        }
        else if (statusInt === 512) {
             "pics/2048/512.png"
        }
        else if (statusInt === 1024) {
             "pics/2048/1024.png"
        }
        else if (statusInt === 2048) {
             expl.explode = true
             "pics/2048/2048.png"
        }
        else if (statusInt === 4096) {
             "pics/2048/4096.png"
        }
        else if (statusInt === 8192) {
             "pics/2048/8192.png"
        }
    }

    Explosion { id: expl }

    property real pauseDur: 250

    transitions: Transition {
        SequentialAnimation {
            PauseAnimation {
                duration: pauseDur
            }
            ScriptAction { script: if (statusInt == 2) { expl.explode = true } }
        }
    }
}

