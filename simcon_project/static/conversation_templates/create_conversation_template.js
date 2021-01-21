//TODO: Validation... field length limits, one start node, maybe all paths lead to terminal?
// Variables used to keep track of state that will eventually get sent to the backend
let templateName = ""           // Holds template's name
let templateDescription = ""    // Holds template's description
let nodes = new Map()           // Map from counter to node. Used to keep track of all the created nodes

// Variables used purely for client side purposes
let unsaved = false             // Indicates if the user made any changes to an INPUT field
let lastUsedNodeIndex = 0       // Counter to be iterated and used as key in nodes map when a new node is created
let currentNodeInFocus = null   // Used to keep track of what node is currently being worked on

// Holds all the information about a single step node
class StepNode {
    constructor() {
        // Items used only for manipulations on the client side
        this.index = 0                      // Used to keep track of node's index in the nodes map (redundant but convenient)
        this.nodeName = ""                  // Node's name
        this.lastChoiceIndex = 0            // Used to keep track of the last choice index used (used as key in responseChoices map below)

        // Items to be propagated to the backend
        this.responseChoices = new Map()    // Array of choices for this node
        this.videoUrl = ""                  // Stores non-embeddable video url (url as user provides it)
        this.nodeDescription = ""           // Node's description
        this.isFirst = false                // True if node is first
        this.isTerminal = false             // True if node is terminal
    }

    // Used when submitting to the backend (when JSON.stringify() is called)
    toJSON() {
        return {
            videoURL: this.videoUrl,
            description: this.nodeDescription,
            isFirst: this.isFirst,
            isTerminal: this.isTerminal,
            responseChoices: Array.from(this.responseChoices.values())
        }
    }
}

// Used inside StepNode to hold available choices at that step
class Choice {
    constructor(description, destinationIndex) {
        this.description = description
        this.destinationIndex = destinationIndex // Stores the node index that serves as the destination for this choice
        // (associated with the 'value' element inside the relevant 'option' in a destination 'select' [look at choice cards])
        // 0 if no destination selected
    }
}

/**
 * Submits constructed nodes objects to the backend effectively creating a new form.
 */
function submit() {

    saveValuesIfNeeded()

    // Retrieves csrftoken
    let csrftoken = null
    const cookieName = 'csrftoken'
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, cookieName.length + 1) === (cookieName + '=')) {
                csrftoken = decodeURIComponent(cookie.substring(cookieName.length + 1));
                break;
            }
        }
    }

    let postBody = JSON.stringify({
        nodes: Array.from(nodes),
        templateName: templateName,
        templateDescription: templateDescription
    })

    // Make POST request
    fetch(window.location.href, {
        method: 'POST',
        credentials: 'include',
        mode: 'same-origin',
        body: postBody,
        headers: new Headers({
           'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        })
    }).then(function(response) {
        if(response.ok) {
            //TODO: handle
        } else throw new Error(response.status)
    }).catch(function (error) {
        //TODO: handle
    })
}

/**
 * Called on page load. Sets the listeners and initializes page content.
 */
function loadState() {
    $(document).ready() //TODO: figure out if calling like this blocks until ready

    addStepNode()
    updateNodeInFocus(1)

    // When an input is changed, change unsaved indicator to true so that the page is saved if another node is put in focus
    $(document).on("change", ":input", function () {
        unsaved = true
    })

    // When step node name is updated, update the state variable and name on the associated step node card
    $(document).on("input", "#node-name-input", function () {
        $("#step-" + currentNodeInFocus.index + " .card-title").text(getNodeNameInput())
    })

    // When a step node card is clicked, that card's context has to be focused
    $(document).on("click", ".step-node-card", function () {
        let clickedNodeId = parseInt($(this).attr('id').split('-')[1])

        if(!(nodes.get(clickedNodeId) === currentNodeInFocus)) {
            updateNodeInFocus(clickedNodeId)
        }
    })

    // Every step node card has a 'Delete' link
    // If click propagation is not stopped, the parent card's onclick event defined above is also triggered when Delete is clicked
    $(document).on("click", ".remove-step-node", function (event) {
        event.stopPropagation()
    })

    // When user updates the video url, updates the embedded video
    $("#video-url-input").blur(() => {
        setEmbeddedVideoUrl(getVideoUrlInput())
    })
}

/**
 * Given a node index, switches focus to it by updating the input and choice data.
 *
 * @param nodeIndex index of the node to be put in focus
 */
function updateNodeInFocus(nodeIndex) {
    saveValuesIfNeeded()

    if(currentNodeInFocus !== null) $("#step-"+currentNodeInFocus.index).css("background-color", "white")
    $("#step-"+nodeIndex).css("background-color", " \t#E8E8E8")

    currentNodeInFocus = nodes.get(nodeIndex)

    document.querySelectorAll('.choice-card').forEach(e => e.remove())
    let currentNodeResponseChoices = currentNodeInFocus.responseChoices
    currentNodeResponseChoices.forEach((value, key) => {
        addChoice(key, value.description, value.destinationIndex)
    })

    setNodeNameInput(currentNodeInFocus.nodeName)
    setNodeDescriptionInput(currentNodeInFocus.nodeDescription)
    setFirstStepToggle(currentNodeInFocus.isFirst)
    setTerminalToggle(currentNodeInFocus.isTerminal)
    setVideoUrlInput(currentNodeInFocus.videoUrl)
    setEmbeddedVideoUrl(currentNodeInFocus.videoUrl)
}

/**
 * Called to save state. Checks if there is state to save before saving.
 */
function saveValuesIfNeeded() {
    if(unsaved) {
        templateName = getTemplateNameInput()
        templateDescription = getTemplateDescriptionInput()

        currentNodeInFocus.videoUrl = getVideoUrlInput()
        currentNodeInFocus.nodeName = getNodeNameInput()
        currentNodeInFocus.nodeDescription = getNodeDescriptionInput()
        currentNodeInFocus.isFirst = getFirstStepToggle()
        currentNodeInFocus.isTerminal = getTerminalToggle()

        document.querySelectorAll('.choice-card').forEach(choice => {
            let currentChoiceId = parseInt(choice.getAttribute('id').split('-')[1])
            let description = choice.getElementsByTagName('textarea')[0].value
            let destination = parseInt(choice.getElementsByTagName('select')[0].value)
            currentNodeInFocus.responseChoices.set(currentChoiceId, new Choice(description, destination))
        })

        unsaved = false
    }
}

/**
 * Adds a step node card to the step node card column and adds a step node to the nodes map
 */
function addStepNode() {
    lastUsedNodeIndex++

    let nodeToAdd = new StepNode()
    nodeToAdd.index = lastUsedNodeIndex
    nodeToAdd.nodeName = String(lastUsedNodeIndex)
    nodes.set(lastUsedNodeIndex, nodeToAdd)

    let newSelectOption = `<option value ="${lastUsedNodeIndex}">${lastUsedNodeIndex}</option>`
    $(".custom-select").append(newSelectOption)

    let stepNodeCard = `
        <div class="card mb-3 step-node-card" id="step-${lastUsedNodeIndex}">
            <div class="card-body">
                <h6 class="card-title">${lastUsedNodeIndex}</h6>
           <!-- <h6 class="card-subtitle mb-2 text-muted">{{ val }}</h6> TODO:Later can be used to display * to indicate changes required-->
                <a href="javascript:removeStep(${lastUsedNodeIndex})" class="card-link remove-step-node">Delete</a>
            </div>
        </div>
    `
    $("#nodes-column .column-button-container:first-child").after(stepNodeCard)
}

/**
 * Removes a step node
 * This involves:
 *      -removing the appropriate card from the step node card column
 *      -updating the choices for all nodes stored in the 'nodes' map to not point to the removed node if they do
 *      -if removed node is in focus changing focus to another card
 *      -if removed node is not in focus, updating currently visible destination selects to not list removed node as an
 *          option and to be unselected if removed node is selected
 *
 * @param nodeIndex
 */
function removeStep(nodeIndex) {

    // Delete the relevant step node card
    let card = document.getElementById("step-" + nodeIndex)
    card.parentElement.removeChild(card)
    nodes.delete(nodeIndex)

    // Update the choices of stored steps to point to 0 if they point to removed step
    nodes.forEach((stepValue, stepIndex) => {
        let choicesOriginal = stepValue.responseChoices
        let choicesCopy = new Map(choicesOriginal)
        choicesCopy.forEach((choiceValue, choiceIndex) => {
            if(choiceValue.destinationIndex == nodeIndex) {
                choicesOriginal.set(choiceIndex, new Choice(choiceValue.description, 0))
            }
        })
    })

    // If removing a node that is not in focus (so step cards will not be rerendered), update selects
    if(nodeIndex != currentNodeInFocus.index) {
        let selects = document.getElementsByTagName("select")
        for(const select of selects) {
            if(select.value == nodeIndex) {
                select.value = 0
            }
            select.removeChild(select.querySelector("[value='" + nodeIndex +"']"))
        }
    } else { // If removing the node that's currently in focus
        if(nodes.size == 0) { // If removing last standing step node
            lastUsedNodeIndex = 0
            addStepNode()
            updateNodeInFocus(1)
        } else { // If there are nodes left to which we can switch focus
            updateNodeInFocus(Array.from(nodes.keys()).reduce((lastKey, currKey) => nodes.get(currKey) !== undefined ? currKey : lastKey))
        }
    }
}

/**
 * Adds a choice card to the choice column
 * If creating a new choice, also adds the choice to the choice map inside current node
 *
 * @param choiceIndex specifies the index of the choice to be added. -1 if adding a new choice
 * @param choiceDescription description of the node
 * @param selectedValue index of the node's destination. O if creating a new node... 0 means unselected
 */
function addChoice(choiceIndex = -1, choiceDescription = "", selectedValue = 0) {
    if(choiceIndex == -1) { // Updates current node's choices map if this function was called to create a new choice
        choiceIndex = ++currentNodeInFocus.lastChoiceIndex
        currentNodeInFocus.responseChoices.set(choiceIndex, new Choice("", 0))
    }

    let htmlToAdd = `
        <div class="card mb-3 choice-card" id="choice-${choiceIndex}">
            <div class="card-body">
            
                <form>
                    <div class="form-group">
                        <label for="choice-description-input">Choice description:</label>
                        <textarea class="form-control" id="node-description-input">${choiceDescription}</textarea>
                    </div>
                </form>
                
            <select class="custom-select">
            ${generateSelectOptions(selectedValue)}
            </select>
            <a href="javascript:removeChoice(${choiceIndex})" class="card-link">Delete</a>
            </div>
        </div>
        `
    $("#choices-column .column-button-container:first-child").after(htmlToAdd)
}

/**
 * Used to generate possible destination options when creating choice cards
 * Marks one choice as 'selected' if 'selectedValue' parameter is not 0
 *
 * @param selectedValue index of the selected destination (0 if none selected)
 * @returns {string} HTML literal wtih the options to be inserted inside an 'insert' element
 */
function generateSelectOptions(selectedValue = 0) {
    let literalToReturn

    if(selectedValue == 0) { // If no destination was selected for this select element, make the select description choice 'selected'
        literalToReturn = `<option disabled selected value="0"> -- select destination -- </option>`
    } else {
        literalToReturn = `<option disabled value="0"> -- select destination -- </option>`
    }

    nodes.forEach((value, key) => {
        if(value !== currentNodeInFocus) {
            if(selectedValue == key) {
                literalToReturn += `<option selected value="${key}">${nodes.get(key).nodeName}</option>`
            } else {
                literalToReturn += `<option value="${key}">${nodes.get(key).nodeName}</option>`
            }
        }
    })
    return literalToReturn
}

/**
 * Used to delete a choice (both from the choice card column and current node's choices map)
 * @param choiceIndex
 */
function removeChoice(choiceIndex) {
    let choiceCard = document.getElementById("choice-" + choiceIndex)
    choiceCard.parentElement.removeChild(choiceCard)
    currentNodeInFocus.responseChoices.delete(choiceIndex)
}

/**
 *
 * @param url YouTube url to embed. Does not have to match embeddable style
 * @returns {string}
 */
function getEmbeddableUrl(url) {
    REGEX = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/
    let match = url.match(REGEX)
    regexedUrl = (match&&match[7].length==11)? match[7] : ""
    if(!(regexedUrl == "")) {
        return "https://www.youtube.com/embed/" + regexedUrl
    }
    return ""
}

// Here are all the DOM getters/setters... technically we don't need standalone functions since most are only used once
// However, we might end up needing them once we are setting up template edit functionality... if not, they can always be moved inline

function getTemplateNameInput() {
    return document.getElementById('template-name-input').value
}

function getTemplateDescriptionInput() {
    return document.getElementById('template-description-input').value
}

function getNodeNameInput() {
    return document.getElementById('node-name-input').value
}

function setNodeNameInput(name) {
    document.getElementById('node-name-input').value = name
}

function getNodeDescriptionInput() {
    return document.getElementById('node-description-input').value
}

function setNodeDescriptionInput(description) {
    document.getElementById('node-description-input').value = description
}

function getFirstStepToggle() {
    return document.getElementById('is-first-node-check').checked
}

function setFirstStepToggle(checked) {
    document.getElementById('is-first-node-check').checked = checked
}

function getTerminalToggle() {
    return document.getElementById('is-terminal-node-check').checked
}

function setTerminalToggle(checked) {
    document.getElementById('is-terminal-node-check').checked = checked
}

function getVideoUrlInput() {
    return document.getElementById('video-url-input').value
}

function setVideoUrlInput(url) {
    document.getElementById('video-url-input').value = url
}

function setEmbeddedVideoUrl(url) {
    document.getElementById("embedded-video-iframe").setAttribute('src', getEmbeddableUrl(url))
}
