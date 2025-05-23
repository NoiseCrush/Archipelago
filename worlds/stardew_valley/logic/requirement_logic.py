import functools
from typing import Iterable

from .base_logic import BaseLogicMixin, BaseLogic
from ..data.game_item import Requirement
from ..data.requirement import ToolRequirement, BookRequirement, SkillRequirement, SeasonRequirement, YearRequirement, CombatRequirement, QuestRequirement, \
    RelationshipRequirement, FishingRequirement, WalnutRequirement, RegionRequirement


class RequirementLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requirement = RequirementLogic(*args, **kwargs)


class RequirementLogic(BaseLogic):

    def meet_all_requirements(self, requirements: Iterable[Requirement]):
        if not requirements:
            return self.logic.true_
        return self.logic.and_(*(self.logic.requirement.meet_requirement(requirement) for requirement in requirements))

    @functools.singledispatchmethod
    def meet_requirement(self, requirement: Requirement):
        raise ValueError(f"Requirements of type{type(requirement)} have no rule registered.")

    @meet_requirement.register
    def _(self, requirement: ToolRequirement):
        return self.logic.tool.has_tool(requirement.tool, requirement.tier)

    @meet_requirement.register
    def _(self, requirement: SkillRequirement):
        return self.logic.skill.has_level(requirement.skill, requirement.level)

    @meet_requirement.register
    def _(self, requirement: RegionRequirement):
        return self.logic.region.can_reach(requirement.region)

    @meet_requirement.register
    def _(self, requirement: BookRequirement):
        return self.logic.book.has_book_power(requirement.book)

    @meet_requirement.register
    def _(self, requirement: SeasonRequirement):
        return self.logic.season.has(requirement.season)

    @meet_requirement.register
    def _(self, requirement: YearRequirement):
        return self.logic.time.has_year(requirement.year)

    @meet_requirement.register
    def _(self, requirement: WalnutRequirement):
        return self.logic.walnut.has_walnut(requirement.amount)

    @meet_requirement.register
    def _(self, requirement: CombatRequirement):
        return self.logic.combat.can_fight_at_level(requirement.level)

    @meet_requirement.register
    def _(self, requirement: QuestRequirement):
        return self.logic.quest.can_complete_quest(requirement.quest)

    @meet_requirement.register
    def _(self, requirement: RelationshipRequirement):
        return self.logic.relationship.has_hearts(requirement.npc, requirement.hearts)

    @meet_requirement.register
    def _(self, requirement: FishingRequirement):
        return self.logic.fishing.can_fish_at(requirement.region)
