const EventSource = require("eventsource")
const Slack = require("slack-node")
require('dotenv').config();

const evtSource = new EventSource("https://utgw.net/nowplaying/stream")

const webhookURL = process.env.WEBHOOK_URL
const slack = new Slack()
slack.setWebhook(webhookURL)
let oldData = {}

const pingMessage = (evt) => {
    slack.webhook({
        channel: "#utgw-kanshi",
        username: "#nowplaying",
        icon_emoji: ":headphones:",
        text: "started."
    }, (err, resp) => {
        console.log(resp)
    })
}

const receiveMessage = (evt) => {
    // console.log(evt)
    const data = JSON.parse(evt.data)
    const title = data.title;
    const artist = data.artist;
    const message = `${title} by ${artist}`
    if (oldData.title !== title) {
        console.log(message)
            oldData = {
                title, artist
            }

        slack.webhook({
            channel: "#utgw-kanshi",
            username: "#nowplaying",
            icon_emoji: ":headphones:",
            text: ":musical_note: " + message
        }, (err, resp) => {
            console.log(resp)
        })
    }
}

evtSource.addEventListener("ping", pingMessage)
evtSource.addEventListener("message", receiveMessage)
