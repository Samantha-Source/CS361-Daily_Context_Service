# CS361-Daily_Context_Service
Daily Context Microservice providing Weather, air-quality, and daylight data

## First user story

### Today’s Context Snapshot

As a user I want to see a snapshot of today’s weather, air quality, and daylight hours so I can decide how to plan my day and habits. 

### Acceptance criteria

#### Functional requirements
Given a request for today’s context, when the endpoint is called, then the service returns weather, air quality, and sunrise/sunset data merged into a single response.
Given one or more underlying sources fails when the request is made, then the service still returns whatever data is available. 

#### Quality attributes & Non-functional requirements
Performance: Response is returned within ~1s
Reliability: Partial results are returned if a source fails.

<br>

## Second user story

### Location Specific Context

As a user I want the daily context to show data specific to my location so that it is relevant to me.

### Acceptance criteria

#### Functional requirements
Given a valid location when the user requests context, then the service returns data specific to that location.
Given an invalid or unrecognized location the service returns a clear error.

#### Quality attributes & Non-functional requirements
Usability: location should accept common formats (city name, zip, lat/long)

