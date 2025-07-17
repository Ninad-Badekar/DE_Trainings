# Cron:
- Cron syntax is used to define time-based job schedules in UNIX systems and tools like Airflow, crontab, Kubernetes CronJobs, etc.
```scss
* * * * * command_to_run
│ │ │ │ │
│ │ │ │ └── Day of the week (0-6) (Sun=0)
│ │ │ └──── Month (1-12)
│ │ └────── Day of the month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)

```
## Example
---
| Expression      | Meaning                         |
| --------------- | ------------------------------- |
| `* * * * *`     | Every minute                    |
| `0 * * * *`     | At the start of every hour      |
| `0 0 * * *`     | At midnight daily               |
| `0 9 * * 1`     | Every Monday at 9:00 AM         |
| `*/15 * * * *`  | Every 15 minutes                |
| `0 0 1 * *`     | At midnight on the 1st of month |
| `0 10,14 * * *` | At 10:00 AM and 2:00 PM daily   |
| `0 0 * * 0`     | Every Sunday at midnight        |

## Special Strings (in cron tab only)

| String     | Equivalent to |
| ---------- | ------------- |
| `@yearly`  | `0 0 1 1 *`   |
| `@monthly` | `0 0 1 * *`   |
| `@weekly`  | `0 0 * * 0`   |
| `@daily`   | `0 0 * * *`   |
| `@hourly`  | `0 * * * *`   |
