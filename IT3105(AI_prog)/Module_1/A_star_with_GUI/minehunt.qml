import QtQuick 1.0
import "GUI_pictures" 1.0

Item {
    id: root
    property int clickx: 0
    property int clicky: 0

    width: 450; height: 500

    Image { source: "GUI_pictures/pics/grey_square.jpg"; anchors.fill: parent; fillMode: Image.Tile }

    Item {
        id: field
        width: parent.width; height: 450
        Grid {
            id: grid
            anchors.centerIn: parent
            columns: numCols; spacing: 5

            Repeater {
                id: repeater
                model: tiles
                delegate: Tile { 
                    width: field.width/numCols - grid.spacing; 
                    height: field.height/numRows - grid.spacing}
            }
        }
    }

    Row {
        id: buttons
        x: 20; spacing: 20
        anchors.top: field.bottom; anchors.bottomMargin: 10; anchors.topMargin: 10; anchors.bottom: root.bottom
        width: root.width

        Image {
            source: "GUI_pictures/pics/quit.png"
            height: parent.height
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: Qt.quit()
            }
        }

        Image {
            source: "GUI_pictures/pics/stop.png"
            height: parent.height
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: resetBoard()
            }
        }
        
        Image { 
            source: "GUI_pictures/pics/play.png" 
            height: parent.height
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: startGame()
            }
        }
        
        Image { 
            source: "GUI_pictures/pics/forward.png"
            height: parent.height
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: updateBoard()
            }
        }
    }
}
