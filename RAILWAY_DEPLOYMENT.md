# Railway Deployment Guide

## Schedule Configuration

The bot supports two ways to configure scheduled tasks (like MOTD):

### Option 1: Environment Variables (Recommended for Railway)

In your Railway project settings, add these environment variables:

- `MOTD_ENABLED=true` (or `false` to disable)
- `MOTD_TIME=12:00` (24-hour format, UTC timezone)

**Note:** Railway runs in UTC by default, so set your time accordingly.

### Option 2: File-based Configuration

Edit `schedule.json` in your repository:

```json
{
  "motd": {
    "enabled": true,
    "time": "12:00"
  }
}
```

**Note:** Times are interpreted as UTC on Railway.

## Timezone Conversion

If you want MOTD to run at a specific local time, convert it to UTC:

- EST (UTC-5): 12:00 EST = 17:00 UTC
- PST (UTC-8): 12:00 PST = 20:00 UTC
- GMT (UTC+0): Same as UTC

## Priority

Environment variables take priority over `schedule.json`. This allows you to:
- Keep default config in the file
- Override with environment variables in Railway without redeploying

