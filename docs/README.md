# Documentation

This directory contains documentation for each GitHub CLI alias in the DE-Utils collection.

## Quick Start Guides

Choose the appropriate setup guide for the tool you want to use:

### [gh prs-md Setup Guide](./gh-prs-md-README.md) 
**First-time setup** for the pull request listing tool.
- Step-by-step installation
- Environment configuration
- Quick diagnostics

### [gh recent-commits Setup Guide](./gh-recent-commits-README.md)
**First-time setup** for the recent commits tool.
- Step-by-step installation  
- Author filtering configuration
- Troubleshooting guide

## Detailed Documentation

For comprehensive usage information after setup:

### [gh prs-md Complete Guide](./gh-prs-md.md)
- Purpose and features
- Advanced configuration
- Customization options
- Troubleshooting

### [gh recent-commits Complete Guide](./gh-recent-commits.md)
- Purpose and features
- Advanced filtering
- Performance considerations
- Integration examples

## Overview

Both tools require:
- **GitHub CLI** (`gh`) - installed and authenticated
- **jq** - JSON processor
- **GH_REPOS** environment variable - list of repositories to query

Additional requirements:
- **gh recent-commits** also requires **COMMIT_AUTHOR** environment variable

## Getting Started

1. **Choose a tool** from the setup guides above
2. **Follow the step-by-step installation** in the README
3. **Test the setup** with the provided examples
4. **Refer to the complete guide** for advanced usage

## Need Help?

- **Start with the setup guides** (README files) for first-time installation
- **Use debug mode** (`DEBUG=1`) to troubleshoot issues
- **Check the complete guides** for advanced features and customization
- **Test individual components** with `gh api` commands if needed
