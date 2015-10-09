import QtQuick 1.0

Image {
    id: flipable
    property int angle: 0

    width: 40;  height: 40
    transform: Rotation { origin.x: width/2; origin.y: height/2; axis.x: 1; axis.z: 0; angle: flipable.angle }

    property int statusInt: modelData.status
    
    source: {
        if (statusInt === 3) {
            "pics/start.png" 
        } 
        else if (statusInt === 4) { 
             "pics/goal.png"
        } 
        else if (statusInt === 5){
            "pics/current.png"
        }
        else if (statusInt === 2) {
            expl.explode = true
            "pics/path.png"
        } 
        else if (statusInt === 1) {
             "pics/opened.png"
        } 
        else if (statusInt === -1) {
             "pics/barrier.png"
        } 
        else {
             "pics/neutral.png"
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

