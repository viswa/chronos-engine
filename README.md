# chronos-engine

# Getting started
Download all dependencies
```
py -m pip install -r requirements.txt
```

Start the app
```
uvicorn main:app --reload
```

Visit [localhost:8000](http://localhost:8000). API Doc at [localhost:8000/docs](http://localhost:8000/docs)

# Usage
Usage of this api should follow something close to what's described below
1. Check for existing timetables by [/exists](http://localhost:8000/exists) path.
2. If so, user can fetch timetables from a zero-indexed array
3. The timetables are session based, so stopping the server wipes any last remaining.
4. Create a timetable by [/create](http://localhost:8000/create)
5. Retrieve a timetable in JSON by [/timetables/{index}](http://localhost:8000/timetable/0)
