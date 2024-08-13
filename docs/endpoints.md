# Common Endpoints

The goal of this library is not to provide a comprehensive interface to the Church
systems, but rather to form a foundation for other projects or scripts. As a
convenience, here are some of the common endpoints that can be used. Shown are the
`ChurchUrl` objects, but the full URL could also be used in the `get_json()` API call.

There are a great many more API endpoints, and the Church changes them from time to
time. If you have additional endpoints, or find one that has changed then please [open
an issue](https://github.com/IsaacsLab42/lcr_session/issues) on GitHub.

## Various Reports

```python title="Actions and Interviews"
ChurchUrl("lcr", "api/umlu/report/action-interview-list/full?unitNumber={unit}")
```

```python title="Assigned Missionaries"
ChurchUrl("lcr", "api/orgs/assigned-missionaries?unitNumber={unit}")
```

```python title="Attendance"
ChurchUrl("lcr", "api/umlu/v1/class-and-quorum/attendance/overview/unitNumber/{unit}")
```

```python title="Birthdays"
ChurchUrl("lcr", "api/report/birthday-list/unit/{unit}?month=1&months=12")
```

```python title="Covenant Path Progress"
ChurchUrl("lcr", "api/report/one-work/progress-record?unitNumber={unit}")
```

```python title="Family History"
ChurchUrl("lcr", "api/report/family-history/activity?unitNumber={unit}")
```

```python title="Full Time Missionaries"
ChurchUrl("lcr", "api/orgs/full-time-missionaries?unitNumber={unit}")
```

```python title="Households"
ChurchUrl("directory", "api/v4/households?unit={unit}")
```

```python title="Member List"
ChurchUrl("lcr", "api/umlu/report/member-list?unitNumber={unit}")
```

```python title="Members With Callings"
ChurchUrl("lcr", "api/report/members-with-callings?unitNumber={unit}")
```

```python title="Members Without Callings"
ChurchUrl("lcr", "api/orgs/members-without-callings?unitNumber={unit}")
```

```python title="Sacrament Meeting Attendance"
ChurchUrl("lcr", "api/sacrament-attendance/unit/{unit}/years/{year}")
```

```python title="Protecting Children and Youth Training"
ChurchUrl("lcr", "api/report/child-protection")
```

```python title="Temple Recommend Status"
ChurchUrl("lcr", "api/temple-recommend/report?unitNumber={unit}")
```
