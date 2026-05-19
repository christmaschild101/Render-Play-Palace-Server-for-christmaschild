# Alerts Extension
This is an extension to the documents system that allows sending read only text dialogs to a user when certain events occur.
For example, display a message when the user logs in, or when they try to access a game that is in beta and not stable.
An alert is a container consisting of an existing document via id, a single event type, an event index (internalized), a dismiss behavior type, and a list of uuids for users who have chosen to dismiss the alert. Depending on the event type, additional fields may be present.

# Backend
Alerts will be apart of the documents system metadata file (server/documents/shared/_metadata.json).

## Alerts section structure
The alerts section would be a json object with each event type being a key, and the value being an array of alerts. Alerts do not have an id or name.
The _metadata.json file would look like this:

{
	"categoies": {},
	"alerts": {
		"user_login": [],
		"beta_table": [],
		"mature_content": [],
		"language_change": []
	}
}

## Alert structure
An example alert would look like this:

{
	"document_id": "motd_20-03-2026",
	"enabled": true,
	"event_type": "user_login",
	"dismiss_behavior": "skippable",
	"dismissed_users": []
}

### Additional fields
Some event types may require extra data such as a list of games for beta table / mature content, or specific locales for language switching.
Typically the first additional field should be referred to as the triggger field, and be named appropriately.

beta_tables:
- triggered_tables: a list of table types aka games that will trigger this alert when the user creates or joins a table of this type. Otherwise the alert will be ignored.

mature_content:
- triggered_content: a list of scenarios that will trigger this alert when the user encounters mature content. Otherwise the alert will be ignored.
*Don't yet know how scenarios should be set. I know that some tables will have mature content, but I want to broaden this to include other scenarios other than creating / joining a table.*

language_change:
- triggered_locales: a list of locales that will trigger this alert when the user switches to these locales. Otherwise the alert will be ignored.

## Available events:
List of available events for this alert to trigger, only one is allowed.
A document can have multiple alerts in case it should be used for more than one event. However an event can not reuse a document, meaning only one alert for this event is allowed for a document.

events:
- user_login: displays when the user logs in.
- beta_table: displays when the user wants to create or join a table that is in beta.
- mature_content: displays when the user creates or joins a table containing mature themes.
- language_change: displays when the user switches to another language.

## Future Dismiss behavior
Controls how the user can prevent this dialog from appearing in the future.
- ephemeral: the dialog is only shown to the user the first time they encounter it, no action needs to be taken.
- skippable: allows the user to select don't show again.
- mandatory: the user can not skip this dialog in the future.

# Frontend
In the documents menu, add a new item called alerts extension. This will only be accessible for admins, and they do not need to be a transcriber.
When clicked, display the list of event types as a menu. No special actions needed, just the list of event types alerts support, and a back action.
Upon clicking on an event type, display the event type x menu.

## Event type x menu
Display all alerts associated with this event type, listed in proper index order.
Alerts are created using existing documents. They do not have their own name or id, rather it uses the document associated with the alert.
An alert would be displayed as: "{localized document name} ({trigger field if any}); {enabled status}"
Trigger field would be a comma separated list.
At the bottom of the menu, add a "new alert" item.
When clicking on an existing alert or new alert, open that alert in the "alert configuration" menu.

## alert configuration menu
For the most part this is self explanitory. List all of the fields of the alert and make them changable. Instead of making a flag for whether or not this is a new alert vs an existin alert, we can simply pass none as the existing alert when creating one.

### document id
If changing the document associated, verify that another alert with this same event type is not alreadyin use with the new selected document.
To select a document, show a list of all documents, without any category filtering. If a document is already selected aka editing an existing alert, focus the menu on the currently selected document. For simplicity, edit the existing show_documents handler to support using this menu from anywhere, and setting initial focus on an item.

### event type
The event type field should not be changable, unless it is a new alert. In which case it won't already have a value, thus should be changable. If existing alert, hide this field.
After the event type field if it exists, add an event index field. This is internalized from the position in the event array.
The index field will allow for changing when this alert triggers vs other alerts of this type. So for example, if the user enters 1 it should show this alert first, and move it to the beginning of the array. Make it 1 based from the user's input.

### Dismiss behavior
Allow for changing the dismiss behavior. After changing, ask if the user wants to clear the list of dismissed users.
After the dismiss behavior field, add a clear dismissed users action if this is an existing alert. Include the number of dismissed users in the string. If 0, give an error when trying to clear. Add a confirmation.

### Delete
At the bottom of the menu, add a "delete alert" action if this is an existing alert. Ask for confirmation.

### Field defaults
If creating a new alert, provide the following defaults:
docuement id = ""
event type = ""
event index = last (current +1)
dismiss behavior = "manditory"
If the user presses back without a document id, consider the operation canceled. If the document id is set but the event type field is empty, require it before saving.

# Edge cases

## Renaming documents
If a document id changes, this will break alerts. Currently there is no way to change a document id from the interface, it has to be renamed on the backend via a file system.
I think this should be addressed later, as it is very unlikely for a document id to change.
I suppose if a document id can't be found when listing alerts, it would warn the user, and ask them to select a new document, but again this isn't immediately important.