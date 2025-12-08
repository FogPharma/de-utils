# GitHub Enterprise SOP Compliance - Implementation Guide

**Status:** For Internal Use
**Created:** [Date]
**Rollout Period:** [Start Date] - [End Date] (2 weeks)

---

## Distribution Plan

1. **Notion Page**: Create main landing page with all three role-specific sections
2. **Email**: Send role-tailored emails to respective audiences
3. **Calendar Invites**: Schedule enablement sessions
4. **GitHub Org Profile**: Add link to compliance page
5. **Internal Portal**: Optional banner announcement

---

## Rollout Schedule

### Week 1 (Days 1-5):
- Baseline audit completed (automated)
- Compliance Scorecard v1 published (automated sync to Notion)
- Exceptions database open for requests
- Org rulesets created and configured (automated enforcement begins)

### Week 2 (Days 6-10):
- Rulesets enabled in audit mode (automated enforcement with reporting)
- Pilot on 5-10 repos
- Automated PRs for standard files opened (automated tools create these)
- Default branch migrations begin (one-time manual work)
- Exception requests processed

### Week 2-3 (Days 11-15):
- Standard files added to all repos (via automated PRs, manual review/merge)
- Branch standardization completed (one-time cleanup)
- Automated stale branch cleanup
- CI/CD workflow updates (manual review required)

### Week 3-4 (Days 16-20):
- Tag workflows implemented (automated workflows trigger on tags)
- Tag seeding for current production versions
- Branch-deploy removal (manual workflow updates)
- Release Views populated (if applicable, automated sync)

### Week 4 (Days 21-28):
- Rulesets enforced on prioritized repos (automated enforcement)
- Final validation and testing
- Enablement sessions delivered
- Recurring audit schedule established (automated nightly audits)

---

## Distribution Checklist

### Pre-Distribution

- [ ] Replace all `[LINK]` placeholders with actual Notion/GitHub URLs
- [ ] Replace `[Date]`, `[Start Date]`, `[End Date]` with actual dates
- [ ] Replace `[compliance-team@fogpharma.com]` with actual email
- [ ] Replace `[#github-compliance]`, `[#github-help]` with actual Slack channels
- [ ] Customize organization name if different from "FogPharma"
- [ ] Review and adjust timeline based on actual sprint schedule
- [ ] Add calendar invite details for enablement sessions

### Notion Distribution

- [ ] Create main landing page in Notion
- [ ] Add all three role-specific sections to the page
- [ ] Link to Compliance Scorecard database
- [ ] Link to Actions & Exceptions database
- [ ] Link to Release Views database (if applicable)
- [ ] Add table of contents for easy navigation
- [ ] Set appropriate page permissions
- [ ] Pin page to relevant workspace sections

### Email Distribution

- [ ] Send "Repo Owners & Administrators" email to:
  - All repository owners (from GitHub API or org directory)
  - All organization admins
  - Engineering leads and managers
- [ ] Send "Contributors & Writers" email to:
  - All GitHub organization members with write access
  - Engineering team distribution list
- [ ] Send "Readers & Users" email to:
  - All organization members
  - Company-wide announcement list (if appropriate)

### Calendar & Events

- [ ] Schedule enablement session for repo owners (1-2 hours)
- [ ] Schedule enablement session for contributors (1 hour)
- [ ] Create calendar invites with:
  - Meeting links (Zoom/Teams)
  - Agenda
  - Links to documentation
  - Q&A time
- [ ] Schedule office hours for questions (recurring weekly for first month)

### GitHub Distribution

- [ ] Update GitHub organization profile with link to compliance page
- [ ] Add compliance link to organization README (if exists)
- [ ] Create `.github/COMPLIANCE.md` file with link (optional)
- [ ] Update organization description/bio with compliance info (optional)

### Internal Portal (Optional)

- [ ] Create banner announcement in internal portal
- [ ] Link to Notion compliance page
- [ ] Set banner to display for 2 weeks
- [ ] Include key dates and action items

### Follow-Up

- [ ] Schedule reminder emails:
  - Week 1: Reminder to review scorecard
  - Week 2: Reminder about enforcement start
  - Week 3: Check-in on progress
- [ ] Monitor exception requests
- [ ] Track compliance score improvements
- [ ] Collect feedback for improvements
- [ ] Schedule retrospective after rollout

---

## Success Metrics

Track these metrics to measure rollout success:
- [ ] % of repos with compliance score >80%
- [ ] Number of exception requests (target: <10% of repos)
- [ ] % of repos with standard files
- [ ] % of repos with proper branch protections
- [ ] Adoption rate of tag-based releases
- [ ] Reduction in direct pushes to `main`
- [ ] Enablement session attendance
- [ ] Support ticket volume

---

## Customization Notes

### Placeholders to Replace

- `[LINK]` - Replace with actual Notion page URLs, GitHub links, etc.
- `[Date]` - Replace with actual date
- `[Start Date]` - Replace with sprint start date
- `[End Date]` - Replace with sprint end date
- `[compliance-team@fogpharma.com]` - Replace with actual compliance team email
- `[#github-compliance]` - Replace with actual Slack channel name
- `[#github-help]` - Replace with actual Slack channel name
- `FogPharma` - Replace with actual organization name if different

### Timeline Adjustments

The timeline assumes a 2-week sprint. Adjust based on:
- Actual sprint duration
- Team capacity
- Number of repositories
- Complexity of existing workflows

### Organization-Specific Customizations

- **Exception Process**: Adjust based on your approval workflow
- **Reviewer Requirements**: May vary by repo size/type
- **CI/CD Details**: Adjust based on your specific CI/CD setup
- **Release Process**: May differ for IaC vs application repos
- **Support Channels**: Use your organization's preferred channels

### Additional Considerations

- **Phased Rollout**: Consider piloting on a subset of repos first
- **Training Materials**: Prepare additional training if needed
- **Migration Support**: Offer help sessions for complex migrations
- **Feedback Loop**: Set up mechanism to collect and address feedback
- **Documentation Updates**: Keep docs updated as policies evolve

---

## Email Templates

### Repository Owners & Administrators

**Subject**: GitHub Enterprise SOP Compliance Rollout - Action Required for Repo Owners

**To:** Github Repository owners and administrators
**Priority:** High
**Timeline:** [Start Date] - [End Date] (2-week sprint)

[Use content from "For Repository Owners & Administrators" section of main communications document]

---

### Contributors & Writers

**Subject**: GitHub Workflow Updates - What You Need to Know

**To:** All GitHub contributors and code writers
**Timeline:** Effective [Start Date], full rollout by [End Date]

[Use content from "For Contributors & Writers" section of main communications document]

---

### Readers & Users

**Subject**: GitHub Standards Update - For Your Information

**To:** All team members
**Timeline:** Rolling out over next 2 weeks

[Use content from "For Readers & Users" section of main communications document]

---

## Implementation Notes

### Automation Setup

- [ ] Configure GitHub organization rulesets
- [ ] Set up automated compliance auditing (nightly runs)
- [ ] Configure repository template with standard files
- [ ] Set up automated PR creation for missing files
- [ ] Configure Notion database integrations
- [ ] Test automation workflows

### Exception Management

- [ ] Set up Notion Actions & Exceptions database
- [ ] Define exception approval workflow
- [ ] Create exception request form/template
- [ ] Assign exception reviewers
- [ ] Set up exception tracking and reporting

### Enablement Materials

- [ ] Create enablement presentation slides
- [ ] Prepare demo repositories/examples
- [ ] Record training videos (optional)
- [ ] Create quick reference cards
- [ ] Prepare FAQ document
- [ ] Set up support channels

### Monitoring & Reporting

- [ ] Set up compliance scorecard dashboard
- [ ] Configure automated reporting (weekly/monthly)
- [ ] Set up alerts for critical compliance gaps
- [ ] Create executive summary reports
- [ ] Track adoption metrics

---

## Rollback Plan

If issues arise during rollout:

1. **Immediate Actions**:
   - Disable rulesets in enforcement mode (switch to audit mode)
   - Pause automated PR creation
   - Communicate status to affected teams

2. **Assessment**:
   - Review exception requests and support tickets
   - Identify root causes of issues
   - Assess impact on development workflows

3. **Remediation**:
   - Adjust ruleset configurations if needed
   - Update documentation based on feedback
   - Provide additional training/support

4. **Resume**:
   - Re-enable rulesets gradually (pilot on subset)
   - Resume automated processes
   - Monitor closely for first week

---

## Post-Rollout

### Week 5+ (Ongoing)

- [ ] Monitor compliance metrics weekly
- [ ] Review exception requests monthly
- [ ] Update documentation based on feedback
- [ ] Conduct quarterly compliance reviews
- [ ] Refine automation based on learnings
- [ ] Plan improvements for next quarter

### Continuous Improvement

- [ ] Collect feedback via surveys
- [ ] Review support ticket patterns
- [ ] Analyze compliance score trends
- [ ] Identify common exception types
- [ ] Update policies based on learnings
- [ ] Share success stories and best practices

