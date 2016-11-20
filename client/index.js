const EventSource = require("eventsource")
const Slack = require("slack-node")

const evtSource = new EventSource("https://utgw.net/nowplaying/stream")

const webhookURL = "your webhook url"
const slack = new Slack()
slack.setWebhook(webhookURL)
slack.webhook({
    channel: "#utgw-kanshi",
    username: "#nowplaying",
    icon_emoji: ":headphones:",
    text: "started."
}, (err, resp) => {
    console.log(resp)
})

const receiveMessage = (evt) => {
    // console.log(evt)
    const data = JSON.parse(evt.data)
    const title = data.title;
    const artist = data.artist;
    const message = `${title} by ${artist}`
    console.log(message)

    slack.webhook({
        channel: "#utgw-kanshi",
        username: "#nowplaying",
        icon_emoji: ":headphones:",
        text: ":musical_note: " + message
    }, (err, resp) => {
        console.log(resp)
    })
}

evtSource.addEventListener("ping", receiveMessage)
evtSource.addEventListener("message", receiveMessage)
