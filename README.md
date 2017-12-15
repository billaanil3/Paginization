# Working with paginated Microsoft Graph responses in Python

![language:Python](https://img.shields.io/badge/Language-Python-blue.svg?style=flat-square) ![license:MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square) 

Some Microsoft Graph queries can return a large number of entities, more than can be included in a single JSON payload. In those cases, Microsoft Graph _paginates_ responses to improve performance. This also makes the response more convenient and flexible for you.

This repo contains Python-based samples that show you how to work with paginated responses in Microsoft Graph. For a high-level overview of how pagination works, see [Paging Microsoft Graph data in your app](https://developer.microsoft.com/en-us/graph/docs/concepts/paging).

The samples in this repo use [messages](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/user_list_messages) to illustrate how pagination works, but the same concepts can be applied to any Microsoft Graph API that uses pagination, including messages, [contacts](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/user_list_contacts), [users](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/user_list), [groups](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/api/group_list), and others.

* [Installation](#installation)
* [Basic concepts](#basic-concepts)
* [Using generators](#using-generators)
* [Contributing](#contributing)
* [Resources](#resources)

## Installation

To install and configure the samples, see the instructions in [Installing the Python REST samples](https://github.com/microsoftgraph/python-sample-auth/blob/master/installation.md). Note that the samples in this repo require **User.Read** and **Mail.Read** permissions.

After you've completed those steps, you'll be able to run the ```pagination.py``` and ```generator.py``` samples as covered below.

## Basic concepts

Pagination for potentially large result sets in Microsoft Graph is based on the [odata.context](http://docs.oasis-open.org/odata/odata-json-format/v4.0/cs01/odata-json-format-v4.0-cs01.html#_Toc365464685) and [odata.nextLink](http://docs.oasis-open.org/odata/odata-json-format/v4.0/cs01/odata-json-format-v4.0-cs01.html#_Toc365464689) annotations that are defined in [OData JSON Format Version 4.0](http://docs.oasis-open.org/odata/odata-json-format/v4.0/cs01/odata-json-format-v4.0-cs01.html).

When you query a paginated Microsoft Graph API (for example, ```me/messages```), you'll get back a JSON payload that contains these top-level elements:

* ```@odata.context``` - Contains a URI that identifies the type of data being returned. This value is the same for every page of the result set.
* ```@odata.nextLink``` - Contains a link to the next page of results. You can do a GET against that endpoint to return the next page, which will contain a link to the next page after that, and you can repeat this process until the final page, which will not have this element.
* ```value``` - Contains the returned data, as a list of JSON elements. In the ```me/messages``` example, this would be a list of email messages. The number of items returned is based on the page size. Each paginated API has a default page size (for example, the ```me/messages``` default is 10 messages), and you can specify a different page size by using the ```$top``` parameter. Note that the default page size and maximum page size might vary for different Microsoft Graph APIs &mdash; see [Paging Microsoft Graph data in your app](https://developer.microsoft.com/en-us/graph/docs/concepts/paging) for more information.

The following diagram shows how this works in practice, using the ```me/messages``` endpoint as an example.

![pagination example](static/images/pagination-example.png)

The [pagination.py](https://github.com/microsoftgraph/python-sample-pagination/blob/master/pagination.py) sample in this repo provides an interactive demonstration of how it works. Follow the [Installation](#installation) instructions to install the sample, and then do the following to run it:

1. At the command prompt: ```python pagination.py```
2. In your browser, go to [http://localhost:5000](http://localhost:5000).
3. Choose **Connect** and authenticate with a Microsoft identity (work or school account or Microsoft account).

You'll then see the following page listing your most recent 10 messages:

![most recent 10 messages](static/images/pagination-sample.png)

The ```@odata.nextLink``` value links to the next page of results. Each time you choose the **Next Page** button, the next page of results is loaded. This is the fundamental behavior of paginated responses from Microsoft Graph APIs.

### What if @odata.nextLink is missing?

In some cases, Graph APIs return all of the requested entities in a single response, and in that case the `@odata.nextLink` element is missing from the response. This may also occur when you have received the last page of data. The absence of this property tells you that there are no more pages of data available in the collection.

For example, if there are fewer than 250 items in your OneDrive root folder, you will see this JSON response when you request all the [DriveItems](https://developer.microsoft.com/en-us/graph/docs/api-reference/v1.0/resources/driveitem) in the folder by doing a GET to the ```https://graph.microsoft.com/v1.0/me/drive/root/children``` endpoint:

![root drive children](static/images/root-drive-children.png)

Because there is no ```@odata.nextLink``` element, you know that this is a complete result set that contains all the requested DriveItems. The default page size for this API is 250 items, so they all fit within a single page of results.

But the same API can return paginated responses, if the result set is larger than the page size. For example, here we're using the ```$top``` query string parameter to return only the first 10 items from the same set:

![pagination via $top parameter](static/images/root-drive-children-top.png)

In this case, the first 10 DriveItems are returned, and you can use an ```@odata.nextLink``` value to query the next page of 10 items.

When working with collections in Graph APIs, your code must always check for `@odata.nextLink` to determine whether there are additional pages of data available, and understand that if the property is missing the result is the last page of available data. There is an example of this in the generator sample below.

## Using generators

The Microsoft Graph API returns _pages_ of results, as demonstrated in [pagination.py](https://github.com/microsoftgraph/python-sample-pagination/blob/master/pagination.py). But in your application or service, you might want to work with a single non-paginated collection of _items_ such as messages, users, or files. This sample creates a Python [generator](https://wiki.python.org/moin/Generators) that hides the pagination details so that your application code can simply ask for a collection of messages and then iterate through them using standard Python idioms such as ```for messages in messages``` or ```next(message)```.

The [generator.py](https://github.com/microsoftgraph/python-sample-pagination/blob/master/generator.py) sample in this repo provides an interactive demonstration of how it works. Follow the [Installation](#installation) instructions to install the sample, and then do the following to run it:

1. At the command prompt: ```python generator.py```
2. In your browser, go to [http://localhost:5000](http://localhost:5000).
3. Choose **Connect** and authenticate with a Microsoft identity (work or school account or Microsoft account).

You'll then see the most recent message you've received:

![most recent message](static/images/generator-sample.png)

Each time you choose **Next Message**, you'll see the next message. The ```generator()``` function in [generator.py](https://github.com/microsoftgraph/python-sample-pagination/blob/master/generator.py) handles the details of retrieving pages of results and then returning (_yielding_) the messages
one at a time.

```python
def graph_generator(session, endpoint=None):
    """Generator for paginated result sets returned by Microsoft Graph.
    session = authenticated Graph session object
    endpoint = the Graph endpoint (for example, 'me/messages' for messages,
               or 'me/drive/root/children' for OneDrive drive items)
    """
    while endpoint:
        print('Retrieving next page ...')
        response = session.get(endpoint).json()
        yield from response.get('value')
        endpoint = response.get('@odata.nextLink')
```

The key concept to understand in this code is the ```yield from``` statement, which returns values from the specified iterator &mdash; ```response.get('value')``` in this case &mdash; until it is exhausted.

To create a generator at runtime, pass the Microsoft Graph session connection object and the API endpoint for retrieving messages:

```python
MSG_GENERATOR = messages(MSGRAPH, 'me/messages')
```

The calling code uses Python's built-in ```next()``` function to retrieve messages:

```python
def generator():
    """Example of using a Python generator to return items from paginated data."""
    return {'graphdata': next(MSG_GENERATOR)}
```

Call ```next(MSG_GENERATOR)``` whenever you need the next message, and you don't need to be aware of the fact that paginated results are coming from Microsoft Graph. You might notice a slightly longer response time whenever a new page is retrieved (every 10th message, with the default page size of 10 messages in the sample), but the individual items within each page are returned immediately without any need to call Microsoft Graph, because they're in the page of results that is being retained in the state of the generator function after each ```yield from``` statement.

Here's an example of the console output that you'll see if you click the **Next Message** button 10 or more times while running the generator sample:

![console output](static/images/console-output.png)

Python generators are recommended for working with all paginated results from Microsoft Graph. You can use the ```generator``` function in this sample for messages, users, groups, drive items, and other paginated responses from Microsoft Graph APIs.

## Contributing

These samples are open source, released under the [MIT License](https://github.com/microsoftgraph/python-sample-pagination/blob/master/LICENSE). Issues (including feature requests and/or questions about this sample) and [pull requests](https://github.com/microsoftgraph/python-sample-pagination/pulls) are welcome. If there's another Python sample you'd like to see for Microsoft Graph, we're interested in that feedback as well &mdash; please log an [issue](https://github.com/microsoftgraph/python-sample-pagination/issues) and let us know!

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). For more information, see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Resources

Documentation:
* [Paging Microsoft Graph data in your app](https://developer.microsoft.com/en-us/graph/docs/concepts/paging)
* [OData JSON Format Version 4.0](http://docs.oasis-open.org/odata/odata-json-format/v4.0/cs01/odata-json-format-v4.0-cs01.html)
* [Python Wiki: Generators](https://wiki.python.org/moin/Generators)

Samples:
* [Python authentication samples for Microsoft Graph](https://github.com/microsoftgraph/python-sample-auth)
* [Sending mail via Microsoft Graph from Python](https://github.com/microsoftgraph/python-sample-send-mail)
* [Working with paginated Microsoft Graph responses in Python](https://github.com/microsoftgraph/python-sample-pagination)
* [Working with Graph open extensions in Python](https://github.com/microsoftgraph/python-sample-open-extensions)
