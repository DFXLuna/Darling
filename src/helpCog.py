
import roleUtil
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.command()
    async def judge_help(self, ctx):
        if await roleUtil.IsValidJudgeContext(ctx, self.bot):
            displayString1 = f"""
Judge commands:
**Grading**:
> `$claim <optionalUuid>` Claim an ungraded submission for judging. Can specify the specific problem with an optional uuid. This must be used in your direct messages OR the judge-grading channel.
> `$unclaim` Remove claim of an ungraded submission. This must be used in your direct messages OR the judge-grading channel.
> `$pass` Passes your currently claimed problem. This must be used in your direct messages OR the judge-grading channel.
> `$fail '<reason>'` Fails your currently claimed problem and send the submitting team the provided quote wrapped message. Your message must be surrounded by quotes. This must be used in your direct messages OR the judge-grading channel.
> `$quick_fail <failureNumber> <optionalExtraNote>` Fails your currently claimed problem and send the submitting team the provided quote wrapped message. Your message must be surrounded by quotes. This must be used in your direct messages OR the judge-grading channel.
> `$quick_fail_reasons` Lists all quick fail reason numbers and the message they correspond to. This must be used in your direct messages OR the judge-grading channel.
> `$list_submissions` Lists all submissions in the database, graded and ungraded. This must be used in your direct messages OR the judge-grading channel.
> `$list_ungraded_submissions` Lists all ungraded submissions in the database. This must be used in your direct messages OR the judge-grading channel.
> `$list_uuids` Lists all submissions with their UUIDs. Useful for claiming a specific problem. This must be used in your direct messages OR the judge-grading channel.
"""
        displayString2 = f"""
**Registration**:
> `$check_registration` Check which team you are registered to. You must DM CodeWarsBot to use this command.
> `$register <teamNumber>` Register yourself to a single team, removes any other registrations. You must DM CodeWarsBot to use this command.
> `$unregister <user#userNumber>` 'Remove user's registration from all times. Use this sparingly. This must be used in your direct messages OR the judge-grading channel.

**Submission**:
> `$submit <problemNumber>` Submit a solution to the given problem number. You must attach your submission file to the message. Mutiple files must be submitted as a zip archive. You must DM CodeWarsBot to use this command.
> `$list_team_submissions​` Lists all of your team's submissions, graded and ungraded. You must DM CodeWarsBot to use this command.

**Help**:
> `$judge_help` Shows this message. This must be used in your direct messages OR the judge-grading channel.
> `$student_help` Shows all commands available to students.
> `$help` Shows the default unhelpful message
"""
        await ctx.send(displayString1 + '\n')
        await ctx.send(displayString2)
        return


    @commands.command()
    async def student_help(self, ctx):
        displayString = f"""
**Registration**:
> `$check_registration` Check which team you are registered to. You must DM CodeWarsBot to use this command.
> `$register <teamNumber>` 'Register yourself to a team. You must DM CodeWarsBot to use this command. If you register yourself to the wrong team, contact Matt Grant and ask him to change your registration. YOU CAN NOT CHANGE YOUR REGISTRATION AFTER THE EVENT STARTS.

**Submission**:
> `$submit <problemNumber>` Submit a solution to the given problem number. You must attach your submission file to the message. Mutiple files must be submitted as a zip archive. You must DM CodeWarsBot to use this command.
> `$list_team_submissions​` Lists all of your team's submissions, graded and ungraded. You must DM CodeWarsBot to use this command.

**Help**:
> `$student_help` Shows this message.
> `$help` Shows the default unhelpful message
"""
        await ctx.send(displayString)