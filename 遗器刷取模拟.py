import random
import json
import pandas as pd
from typing import List, Tuple, Dict
from dataclasses import dataclass
from enum import Enum

class RelicType(Enum):
    """遗器类型枚举"""
    OUTER = "外圈遗器"
    INNER = "内圈遗器"

class RelicSlot(Enum):
    """遗器部位枚举"""
    # 外圈遗器部位
    HEAD = "头"
    HANDS = "手"
    BODY = "衣服"
    FEET = "鞋子"
    # 内圈遗器部位
    SPHERE = "球"
    ROPE = "绳子"

class MainStatType(Enum):
    """主词条类型枚举"""
    HP = "生命"
    ATK = "攻击"
    DEF = "防御"
    HP_PERCENT = "生命百分比"
    ATK_PERCENT = "攻击百分比"
    DEF_PERCENT = "防御百分比"
    CRIT_RATE = "暴击"
    CRIT_DMG = "暴伤"
    HEALING = "治疗"
    EFFECT_HIT = "命中"
    SPD = "速度"
    BREAK_EFFECT = "击破"
    ENERGY_RECHARGE = "充能"
    # 属性伤害
    PHYSICAL_DMG = "物理伤害"
    FIRE_DMG = "火伤害"
    WIND_DMG = "风伤害"
    ICE_DMG = "冰伤害"
    LIGHTNING_DMG = "雷伤害"
    QUANTUM_DMG = "量子伤害"
    IMAGINARY_DMG = "虚数伤害"

class SubStatType(Enum):
    """副词条类型枚举"""
    HP = "生命"
    ATK = "攻击"
    DEF = "防御"
    HP_PERCENT = "生命百分比"
    ATK_PERCENT = "攻击百分比"
    DEF_PERCENT = "防御百分比"
    SPD = "速度"
    CRIT_RATE = "暴击"
    CRIT_DMG = "暴伤"
    EFFECT_HIT = "命中"
    EFFECT_RES = "抵抗"
    BREAK_EFFECT = "击破"

@dataclass
class SubStat:
    """副词条类"""
    stat_type: SubStatType
    value: float
    is_percentage: bool = False
    
    def __str__(self):
        if self.is_percentage:
            return f"{self.stat_type.value} {self.value:.3f}%"
        else:
            return f"{self.stat_type.value} {self.value:.3f}"

@dataclass
class RelicSet:
    """遗器套装类"""
    name: str
    relic_type: RelicType
    description: str = ""

@dataclass
class Relic:
    """遗器类"""
    set_name: str
    relic_type: RelicType
    slot: RelicSlot
    main_stat: MainStatType
    main_stat_value: float = 0.0
    sub_stats: List[SubStat] = None
    enhancement_level: int = 0  # 强化等级
    sub_stat_counts: Dict[SubStatType, int] = None  # 副词条词条数统计
    
    def __post_init__(self):
        if self.sub_stats is None:
            self.sub_stats = []
        if self.sub_stat_counts is None:
            self.sub_stat_counts = {}
    
    def get_sub_stat_count(self, stat_type: SubStatType) -> int:
        """获取指定副词条类型的词条数"""
        return self.sub_stat_counts.get(stat_type, 0)
    
    def add_sub_stat_count(self, stat_type: SubStatType, count: int = 1):
        """增加指定副词条类型的词条数"""
        self.sub_stat_counts[stat_type] = self.sub_stat_counts.get(stat_type, 0) + count

class RelicFarmSimulator:
    """遗器刷取模拟器"""
    
    def __init__(self):
        # 初始化外圈遗器套装
        self.outer_relic_sets = [
            RelicSet("风套", RelicType.OUTER, "风属性伤害加成"),
            RelicSet("冰套", RelicType.OUTER, "冰属性伤害加成"),
            RelicSet("量子套", RelicType.OUTER, "量子伤害加成"),
            RelicSet("铁卫套", RelicType.OUTER, "铁卫套装效果"),
            RelicSet("勇烈套", RelicType.OUTER, "勇烈套装效果"),
            RelicSet("铁骑套", RelicType.OUTER, "铁骑套装效果"),
            RelicSet("司铎套", RelicType.OUTER, "司铎套装效果"),
            RelicSet("学者套", RelicType.OUTER, "学者套装效果"),
        ]
        
        # 初始化内圈遗器套装
        self.inner_relic_sets = [
            RelicSet("翁瓦克", RelicType.INNER, "翁瓦克套装效果"),
            RelicSet("塔利亚", RelicType.INNER, "塔利亚套装效果"),
            RelicSet("劫火", RelicType.INNER, "劫火套装效果"),
            RelicSet("奔狼", RelicType.INNER, "奔狼套装效果"),
            RelicSet("蕉乐园", RelicType.INNER, "蕉乐园套装效果"),
            RelicSet("露莎卡", RelicType.INNER, "露莎卡套装效果"),
            RelicSet("巨树", RelicType.INNER, "巨树套装效果"),
            RelicSet("拾骨地", RelicType.INNER, "拾骨地套装效果"),
        ]
        
        # 预计算主词条排除映射，避免重复计算
        self.main_stat_exclusion_map = {
            MainStatType.HP: SubStatType.HP,
            MainStatType.ATK: SubStatType.ATK,
            MainStatType.DEF: SubStatType.DEF,
            MainStatType.HP_PERCENT: SubStatType.HP_PERCENT,
            MainStatType.ATK_PERCENT: SubStatType.ATK_PERCENT,
            MainStatType.DEF_PERCENT: SubStatType.DEF_PERCENT,
            MainStatType.CRIT_RATE: SubStatType.CRIT_RATE,
            MainStatType.CRIT_DMG: SubStatType.CRIT_DMG,
            MainStatType.EFFECT_HIT: SubStatType.EFFECT_HIT,
            MainStatType.BREAK_EFFECT: SubStatType.BREAK_EFFECT,
            MainStatType.SPD: SubStatType.SPD,
        }
        
        # 副本配置：每个副本包含两种套装
        self.dungeons = {
            "外圈副本1": [self.outer_relic_sets[0], self.outer_relic_sets[1]],  # 风套 + 冰套
            "外圈副本2": [self.outer_relic_sets[2], self.outer_relic_sets[3]],  # 量子套 + 铁卫套
            "外圈副本3": [self.outer_relic_sets[4], self.outer_relic_sets[5]],  # 勇烈套 + 铁骑套
            "外圈副本4": [self.outer_relic_sets[6], self.outer_relic_sets[7]],  # 司铎套 + 学者套
            
            "内圈副本1": [self.inner_relic_sets[0], self.inner_relic_sets[1]],  # 翁瓦克 + 塔利亚
            "内圈副本2": [self.inner_relic_sets[2], self.inner_relic_sets[3]],  # 劫火 + 奔狼
            "内圈副本3": [self.inner_relic_sets[4], self.inner_relic_sets[5]],  # 蕉乐园 + 露莎卡
            "内圈副本4": [self.inner_relic_sets[6], self.inner_relic_sets[7]],  # 巨树 + 拾骨地
        }
        
        # 外圈遗器部位
        self.outer_slots = [RelicSlot.HEAD, RelicSlot.HANDS, RelicSlot.BODY, RelicSlot.FEET]
        
        # 内圈遗器部位
        self.inner_slots = [RelicSlot.SPHERE, RelicSlot.ROPE]
        
        # 属性伤害类型
        self.elemental_dmg_types = [
            MainStatType.PHYSICAL_DMG,
            MainStatType.FIRE_DMG,
            MainStatType.WIND_DMG,
            MainStatType.ICE_DMG,
            MainStatType.LIGHTNING_DMG,
            MainStatType.QUANTUM_DMG,
            MainStatType.IMAGINARY_DMG
        ]
        
        # 副词条权重系统
        self.sub_stat_weights = {
            SubStatType.HP: 100,
            SubStatType.ATK: 100,
            SubStatType.DEF: 100,
            SubStatType.HP_PERCENT: 100,
            SubStatType.ATK_PERCENT: 100,
            SubStatType.DEF_PERCENT: 100,
            SubStatType.SPD: 40,
            SubStatType.CRIT_RATE: 60,
            SubStatType.CRIT_DMG: 60,
            SubStatType.EFFECT_HIT: 80,
            SubStatType.EFFECT_RES: 80,
            SubStatType.BREAK_EFFECT: 80,
        }
        
        # 副词条数值档位系统
        self.sub_stat_values = {
            SubStatType.HP: [33.870, 38.104, 42.338],
            SubStatType.ATK: [16.935, 19.052, 21.169],
            SubStatType.DEF: [16.935, 19.052, 21.169],
            SubStatType.HP_PERCENT: [3.456, 3.888, 4.320],
            SubStatType.ATK_PERCENT: [3.456, 3.888, 4.320],
            SubStatType.DEF_PERCENT: [4.320, 4.860, 5.400],
            SubStatType.SPD: [2.0, 2.3, 2.6],
            SubStatType.CRIT_RATE: [2.592, 2.916, 3.240],
            SubStatType.CRIT_DMG: [5.184, 5.832, 6.480],
            SubStatType.EFFECT_HIT: [3.456, 3.888, 4.320],
            SubStatType.EFFECT_RES: [3.456, 3.888, 4.320],
            SubStatType.BREAK_EFFECT: [5.184, 5.832, 6.480],
        }
        
        # 副词条是否为百分比类型
        self.sub_stat_percentage_types = {
            SubStatType.HP_PERCENT, SubStatType.ATK_PERCENT, SubStatType.DEF_PERCENT,
            SubStatType.CRIT_RATE, SubStatType.CRIT_DMG, SubStatType.EFFECT_HIT,
            SubStatType.EFFECT_RES, SubStatType.BREAK_EFFECT
        }
    
    def get_random_slot(self, relic_type: RelicType) -> RelicSlot:
        """根据遗器类型随机选择部位"""
        if relic_type == RelicType.OUTER:
            return random.choice(self.outer_slots)
        else:
            return random.choice(self.inner_slots)
    
    def get_main_stat_for_slot(self, slot: RelicSlot) -> MainStatType:
        """根据部位获取主词条"""
        if slot == RelicSlot.HEAD:
            return MainStatType.HP
        elif slot == RelicSlot.HANDS:
            return MainStatType.ATK
        elif slot == RelicSlot.BODY:
            # 衣服主词条概率分配
            rand = random.random()
            if rand < 0.2:
                return MainStatType.HP_PERCENT
            elif rand < 0.4:
                return MainStatType.ATK_PERCENT
            elif rand < 0.6:
                return MainStatType.DEF_PERCENT
            elif rand < 0.7:
                return MainStatType.CRIT_RATE
            elif rand < 0.8:
                return MainStatType.CRIT_DMG
            elif rand < 0.9:
                return MainStatType.HEALING
            else:
                return MainStatType.EFFECT_HIT
        elif slot == RelicSlot.FEET:
            # 鞋子主词条概率分配
            rand = random.random()
            if rand < 0.28:
                return MainStatType.HP_PERCENT
            elif rand < 0.58:
                return MainStatType.ATK_PERCENT
            elif rand < 0.875:
                return MainStatType.DEF_PERCENT
            else:
                return MainStatType.SPD
        elif slot == RelicSlot.SPHERE:
            # 球主词条概率分配
            rand = random.random()
            if rand < 0.125:
                return MainStatType.HP_PERCENT
            elif rand < 0.25:
                return MainStatType.ATK_PERCENT
            elif rand < 0.37:
                return MainStatType.DEF_PERCENT
            else:
                # 63%概率为属性伤害，7种属性概率均等
                return random.choice(self.elemental_dmg_types)
        elif slot == RelicSlot.ROPE:
            # 绳子主词条概率分配
            rand = random.random()
            if rand < 0.27:
                return MainStatType.HP_PERCENT
            elif rand < 0.54:
                return MainStatType.ATK_PERCENT
            elif rand < 0.79:
                return MainStatType.DEF_PERCENT
            elif rand < 0.94:
                return MainStatType.BREAK_EFFECT
            else:
                return MainStatType.ENERGY_RECHARGE
        else:
            raise ValueError(f"未知的部位: {slot}")
    
    def get_sub_stats(self, main_stat: MainStatType, sub_stat_count: int) -> List[SubStat]:
        """根据主词条和副词条数量抽取副词条"""
        # 创建可选的副词条列表（排除主词条）
        available_sub_stats = []
        available_weights = []
        
        for sub_stat, weight in self.sub_stat_weights.items():
            # 排除主词条对应的副词条
            if self._is_main_stat_excluded(main_stat, sub_stat):
                continue
            available_sub_stats.append(sub_stat)
            available_weights.append(weight)
        
        # 不放回抽取指定数量的副词条
        selected_sub_stats = []
        for _ in range(sub_stat_count):
            if not available_sub_stats:
                break
            
            # 根据权重随机选择
            chosen_index = random.choices(
                range(len(available_sub_stats)), 
                weights=available_weights, 
                k=1
            )[0]
            
            chosen_sub_stat_type = available_sub_stats[chosen_index]
            
            # 随机选择数值档位
            value_tiers = self.sub_stat_values[chosen_sub_stat_type]
            chosen_value = random.choice(value_tiers)
            
            # 判断是否为百分比类型
            is_percentage = chosen_sub_stat_type in self.sub_stat_percentage_types
            
            # 创建副词条对象
            sub_stat = SubStat(
                stat_type=chosen_sub_stat_type,
                value=chosen_value,
                is_percentage=is_percentage
            )
            
            selected_sub_stats.append(sub_stat)
            
            # 从可选列表中移除已选择的副词条
            available_sub_stats.pop(chosen_index)
            available_weights.pop(chosen_index)
        
        return selected_sub_stats
    
    def enhance_relic(self, relic: Relic, times: int = 1) -> Relic:
        """强化遗器"""
        for _ in range(times):
            if len(relic.sub_stats) < 4:
                # 副词条数量不足4个，新增一个副词条
                self._add_new_sub_stat(relic)
            else:
                # 副词条数量已满，随机强化一个副词条
                self._enhance_random_sub_stat(relic)
            relic.enhancement_level += 1
        return relic
    
    def _add_new_sub_stat(self, relic: Relic):
        """为遗器新增一个副词条"""
        # 获取已有的副词条类型
        existing_sub_stat_types = {stat.stat_type for stat in relic.sub_stats}
        
        # 创建可选的副词条列表（排除主词条和已有副词条）
        available_sub_stats = []
        available_weights = []
        
        for sub_stat_type, weight in self.sub_stat_weights.items():
            # 排除主词条对应的副词条
            if self._is_main_stat_excluded(relic.main_stat, sub_stat_type):
                continue
            # 排除已有的副词条
            if sub_stat_type in existing_sub_stat_types:
                continue
            available_sub_stats.append(sub_stat_type)
            available_weights.append(weight)
        
        if not available_sub_stats:
            return  # 没有可选的副词条
        
        # 根据权重随机选择
        chosen_sub_stat_type = random.choices(
            available_sub_stats,
            weights=available_weights,
            k=1
        )[0]
        
        # 随机选择数值档位
        value_tiers = self.sub_stat_values[chosen_sub_stat_type]
        chosen_value = random.choice(value_tiers)
        
        # 判断是否为百分比类型
        is_percentage = chosen_sub_stat_type in self.sub_stat_percentage_types
        
        # 创建新的副词条
        new_sub_stat = SubStat(
            stat_type=chosen_sub_stat_type,
            value=chosen_value,
            is_percentage=is_percentage
        )
        
        relic.sub_stats.append(new_sub_stat)
        # 增加词条数统计
        relic.add_sub_stat_count(chosen_sub_stat_type)
    
    def _enhance_random_sub_stat(self, relic: Relic):
        """随机强化一个副词条"""
        if not relic.sub_stats:
            return
        
        # 随机选择一个副词条
        chosen_sub_stat = random.choice(relic.sub_stats)
        
        # 随机选择新的数值档位
        value_tiers = self.sub_stat_values[chosen_sub_stat.stat_type]
        new_value = random.choice(value_tiers)
        
        # 在原有数值上累加
        chosen_sub_stat.value += new_value
        
        # 增加词条数统计
        relic.add_sub_stat_count(chosen_sub_stat.stat_type)
    
    def _is_main_stat_excluded(self, main_stat: MainStatType, sub_stat: SubStatType) -> bool:
        """判断主词条是否应该排除对应的副词条"""
        # 主词条和副词条的对应关系
        exclusion_map = {
            MainStatType.HP: SubStatType.HP,
            MainStatType.ATK: SubStatType.ATK,
            MainStatType.DEF: SubStatType.DEF,
            MainStatType.HP_PERCENT: SubStatType.HP_PERCENT,
            MainStatType.ATK_PERCENT: SubStatType.ATK_PERCENT,
            MainStatType.DEF_PERCENT: SubStatType.DEF_PERCENT,
            MainStatType.CRIT_RATE: SubStatType.CRIT_RATE,
            MainStatType.CRIT_DMG: SubStatType.CRIT_DMG,
            MainStatType.EFFECT_HIT: SubStatType.EFFECT_HIT,
            MainStatType.BREAK_EFFECT: SubStatType.BREAK_EFFECT,
            MainStatType.SPD: SubStatType.SPD,
        }
        
        return exclusion_map.get(main_stat) == sub_stat
    
    def load_config(self, config_file: str) -> Dict:
        """加载JSON配置文件"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def check_relic_filter(self, relic: Relic, filter_condition: Dict) -> bool:
        """检查遗器是否符合筛选条件"""
        # 检查套装
        if filter_condition.get("套装") and relic.set_name != filter_condition["套装"]:
            return False
        
        # 检查部位
        if filter_condition.get("部位"):
            slot_name = filter_condition["部位"]
            if slot_name == "头" and relic.slot != RelicSlot.HEAD:
                return False
            elif slot_name == "手" and relic.slot != RelicSlot.HANDS:
                return False
            elif slot_name == "衣服" and relic.slot != RelicSlot.BODY:
                return False
            elif slot_name == "鞋子" and relic.slot != RelicSlot.FEET:
                return False
            elif slot_name == "球" and relic.slot != RelicSlot.SPHERE:
                return False
            elif slot_name == "绳子" and relic.slot != RelicSlot.ROPE:
                return False
        
        # 检查主属性
        if filter_condition.get("主属性"):
            main_stat_name = filter_condition["主属性"]
            if main_stat_name == "生命" and relic.main_stat != MainStatType.HP:
                return False
            elif main_stat_name == "攻击" and relic.main_stat != MainStatType.ATK:
                return False
            elif main_stat_name == "防御" and relic.main_stat != MainStatType.DEF:
                return False
            elif main_stat_name == "生命百分比" and relic.main_stat != MainStatType.HP_PERCENT:
                return False
            elif main_stat_name == "攻击百分比" and relic.main_stat != MainStatType.ATK_PERCENT:
                return False
            elif main_stat_name == "防御百分比" and relic.main_stat != MainStatType.DEF_PERCENT:
                return False
            elif main_stat_name == "暴击" and relic.main_stat != MainStatType.CRIT_RATE:
                return False
            elif main_stat_name == "暴伤" and relic.main_stat != MainStatType.CRIT_DMG:
                return False
            elif main_stat_name == "治疗" and relic.main_stat != MainStatType.HEALING:
                return False
            elif main_stat_name == "命中" and relic.main_stat != MainStatType.EFFECT_HIT:
                return False
            elif main_stat_name == "速度" and relic.main_stat != MainStatType.SPD:
                return False
            elif main_stat_name == "击破" and relic.main_stat != MainStatType.BREAK_EFFECT:
                return False
            elif main_stat_name == "充能" and relic.main_stat != MainStatType.ENERGY_RECHARGE:
                return False
            # 检查属性伤害类型
            elif main_stat_name == "物理" and relic.main_stat != MainStatType.PHYSICAL_DMG:
                return False
            elif main_stat_name == "火" and relic.main_stat != MainStatType.FIRE_DMG:
                return False
            elif main_stat_name == "风" and relic.main_stat != MainStatType.WIND_DMG:
                return False
            elif main_stat_name == "冰" and relic.main_stat != MainStatType.ICE_DMG:
                return False
            elif main_stat_name == "雷" and relic.main_stat != MainStatType.LIGHTNING_DMG:
                return False
            elif main_stat_name == "量子" and relic.main_stat != MainStatType.QUANTUM_DMG:
                return False
            elif main_stat_name == "虚数" and relic.main_stat != MainStatType.IMAGINARY_DMG:
                return False
        
        return True
    
    def calculate_effective_sub_stats(self, relic: Relic, effective_sub_stats: List[str]) -> int:
        """计算有效副词条数量"""
        total_count = 0
        for stat_name in effective_sub_stats:
            if stat_name == "暴击":
                total_count += relic.get_sub_stat_count(SubStatType.CRIT_RATE)
            elif stat_name == "暴伤":
                total_count += relic.get_sub_stat_count(SubStatType.CRIT_DMG)
            elif stat_name == "速度":
                total_count += relic.get_sub_stat_count(SubStatType.SPD)
            elif stat_name == "生命":
                total_count += relic.get_sub_stat_count(SubStatType.HP)
            elif stat_name == "攻击":
                total_count += relic.get_sub_stat_count(SubStatType.ATK)
            elif stat_name == "防御":
                total_count += relic.get_sub_stat_count(SubStatType.DEF)
            elif stat_name == "生命百分比":
                total_count += relic.get_sub_stat_count(SubStatType.HP_PERCENT)
            elif stat_name == "攻击百分比":
                total_count += relic.get_sub_stat_count(SubStatType.ATK_PERCENT)
            elif stat_name == "防御百分比":
                total_count += relic.get_sub_stat_count(SubStatType.DEF_PERCENT)
            elif stat_name == "命中":
                total_count += relic.get_sub_stat_count(SubStatType.EFFECT_HIT)
            elif stat_name == "抵抗":
                total_count += relic.get_sub_stat_count(SubStatType.EFFECT_RES)
            elif stat_name == "击破":
                total_count += relic.get_sub_stat_count(SubStatType.BREAK_EFFECT)
        
        return total_count
    
    def find_best_relics(self, all_relics: List[Relic], filter_conditions: List[Dict], effective_sub_stats: List[str]) -> Dict[str, Relic]:
        """找到各个部位符合筛选条件的有效副词条数最多的遗器"""
        best_relics = {}
        
        for relic in all_relics:
            # 检查是否符合任一筛选条件
            matched_condition = None
            for condition in filter_conditions:
                if self.check_relic_filter(relic, condition):
                    matched_condition = condition
                    break
            
            if matched_condition:
                # 计算有效副词条数量
                effective_count = self.calculate_effective_sub_stats(relic, effective_sub_stats)
                
                # 获取部位名称
                slot_name = relic.slot.value
                
                # 如果该部位还没有最佳遗器，或者当前遗器的有效副词条数更多
                if slot_name not in best_relics or effective_count > self.calculate_effective_sub_stats(best_relics[slot_name], effective_sub_stats):
                    best_relics[slot_name] = relic
        
        return best_relics
    
    def create_relic(self, set_name: str, relic_type: RelicType) -> Relic:
        """创建一个遗器"""
        slot = self.get_random_slot(relic_type)
        main_stat = self.get_main_stat_for_slot(slot)
        
        # 确定副词条数量
        sub_stat_count = 4 if random.random() < 0.2 else 3
        
        # 抽取副词条
        sub_stats = self.get_sub_stats(main_stat, sub_stat_count)
        
        # 创建遗器并初始化词条数统计
        relic = Relic(
            set_name=set_name,
            relic_type=relic_type,
            slot=slot,
            main_stat=main_stat,
            sub_stats=sub_stats
        )
        
        # 统计初始副词条词条数
        for sub_stat in sub_stats:
            relic.add_sub_stat_count(sub_stat.stat_type)
        
        return relic
    
    def create_relic_optimized(self, set_name: str, relic_type: RelicType) -> Relic:
        """优化版本：创建一个遗器，减少对象创建开销"""
        # 直接使用random.choice而不是get_random_slot
        if relic_type == RelicType.OUTER:
            slot = random.choice(self.outer_slots)
        else:
            slot = random.choice(self.inner_slots)
        
        # 直接计算主词条，避免函数调用开销
        main_stat = self._get_main_stat_for_slot_fast(slot)
        
        # 确定副词条数量
        sub_stat_count = 4 if random.random() < 0.2 else 3
        
        # 抽取副词条
        sub_stats = self._get_sub_stats_fast(main_stat, sub_stat_count)
        
        # 创建遗器并初始化词条数统计
        relic = Relic(
            set_name=set_name,
            relic_type=relic_type,
            slot=slot,
            main_stat=main_stat,
            sub_stats=sub_stats
        )
        
        # 统计初始副词条词条数
        for sub_stat in sub_stats:
            relic.add_sub_stat_count(sub_stat.stat_type)
        
        return relic
    
    def _get_main_stat_for_slot_fast(self, slot: RelicSlot) -> MainStatType:
        """快速版本：根据部位获取主词条，减少函数调用开销"""
        if slot == RelicSlot.HEAD:
            return MainStatType.HP
        elif slot == RelicSlot.HANDS:
            return MainStatType.ATK
        elif slot == RelicSlot.BODY:
            # 衣服主词条概率分配
            rand = random.random()
            if rand < 0.2:
                return MainStatType.HP_PERCENT
            elif rand < 0.4:
                return MainStatType.ATK_PERCENT
            elif rand < 0.6:
                return MainStatType.DEF_PERCENT
            elif rand < 0.7:
                return MainStatType.CRIT_RATE
            elif rand < 0.8:
                return MainStatType.CRIT_DMG
            elif rand < 0.9:
                return MainStatType.HEALING
            else:
                return MainStatType.EFFECT_HIT
        elif slot == RelicSlot.FEET:
            # 鞋子主词条概率分配
            rand = random.random()
            if rand < 0.28:
                return MainStatType.HP_PERCENT
            elif rand < 0.58:
                return MainStatType.ATK_PERCENT
            elif rand < 0.875:
                return MainStatType.DEF_PERCENT
            else:
                return MainStatType.SPD
        elif slot == RelicSlot.SPHERE:
            # 球主词条概率分配
            rand = random.random()
            if rand < 0.125:
                return MainStatType.HP_PERCENT
            elif rand < 0.25:
                return MainStatType.ATK_PERCENT
            elif rand < 0.37:
                return MainStatType.DEF_PERCENT
            else:
                # 63%概率为属性伤害，7种属性概率均等
                return random.choice(self.elemental_dmg_types)
        elif slot == RelicSlot.ROPE:
            # 绳子主词条概率分配
            rand = random.random()
            if rand < 0.27:
                return MainStatType.HP_PERCENT
            elif rand < 0.54:
                return MainStatType.ATK_PERCENT
            elif rand < 0.79:
                return MainStatType.DEF_PERCENT
            elif rand < 0.94:
                return MainStatType.BREAK_EFFECT
            else:
                return MainStatType.ENERGY_RECHARGE
        else:
            raise ValueError(f"未知的部位: {slot}")
    
    def _get_sub_stats_fast(self, main_stat: MainStatType, sub_stat_count: int) -> List[SubStat]:
        """快速版本：根据主词条和副词条数量抽取副词条，减少函数调用开销"""
        # 使用预计算的排除映射
        excluded_sub_stat = self.main_stat_exclusion_map.get(main_stat)
        
        # 创建可选的副词条列表（排除主词条）
        available_sub_stats = []
        available_weights = []
        
        for sub_stat, weight in self.sub_stat_weights.items():
            # 排除主词条对应的副词条
            if sub_stat == excluded_sub_stat:
                continue
            available_sub_stats.append(sub_stat)
            available_weights.append(weight)
        
        # 不放回抽取指定数量的副词条
        selected_sub_stats = []
        for _ in range(sub_stat_count):
            if not available_sub_stats:
                break
            
            # 根据权重随机选择
            chosen_index = random.choices(
                range(len(available_sub_stats)), 
                weights=available_weights, 
                k=1
            )[0]
            
            chosen_sub_stat_type = available_sub_stats[chosen_index]
            
            # 随机选择数值档位
            value_tiers = self.sub_stat_values[chosen_sub_stat_type]
            chosen_value = random.choice(value_tiers)
            
            # 判断是否为百分比类型
            is_percentage = chosen_sub_stat_type in self.sub_stat_percentage_types
            
            # 创建副词条对象
            sub_stat = SubStat(
                stat_type=chosen_sub_stat_type,
                value=chosen_value,
                is_percentage=is_percentage
            )
            
            selected_sub_stats.append(sub_stat)
            
            # 从可选列表中移除已选择的副词条
            available_sub_stats.pop(chosen_index)
            available_weights.pop(chosen_index)
        
        return selected_sub_stats
    
    def farm_relics(self, dungeon_name: str, times: int = 1, enhance: bool = False) -> List[Dict]:
        """
        在指定副本刷取遗器
        
        Args:
            dungeon_name: 副本名称
            times: 刷取次数
            enhance: 是否立即强化到+5
            
        Returns:
            刷取结果列表
        """
        if dungeon_name not in self.dungeons:
            raise ValueError(f"副本 {dungeon_name} 不存在")
        
        results = []
        available_sets = self.dungeons[dungeon_name]  # 预获取可用套装
        
        for _ in range(times):
            # 确定本次刷取获得的遗器数量
            relic_count = 3 if random.random() < 0.1 else 2
            
            # 为每个遗器随机选择套装并创建遗器
            farm_result = []
            for _ in range(relic_count):
                chosen_set = random.choice(available_sets)
                relic = self.create_relic_optimized(chosen_set.name, chosen_set.relic_type)
                
                # 如果开启强化，立即强化到+5
                if enhance:
                    relic = self.enhance_relic(relic, 5)
                
                farm_result.append(relic)
            
            results.append({
                "dungeon": dungeon_name,
                "relic_count": relic_count,
                "relics": farm_result
            })
        
        return results
    
    def _farm_relics_fast(self, available_sets: List[RelicSet], times: int, enhance: bool) -> List[Relic]:
        """快速版本：在指定副本刷取遗器，直接返回遗器列表"""
        all_relics = []
        
        for _ in range(times):
            # 确定本次刷取获得的遗器数量
            relic_count = 3 if random.random() < 0.1 else 2
            
            # 为每个遗器随机选择套装并创建遗器
            for _ in range(relic_count):
                chosen_set = random.choice(available_sets)
                relic = self.create_relic_optimized(chosen_set.name, chosen_set.relic_type)
                
                # 如果开启强化，立即强化到+5
                if enhance:
                    relic = self.enhance_relic(relic, 5)
                
                all_relics.append(relic)
        
        return all_relics
    
    def print_farm_results(self, results: List[Dict]):
        """打印刷取结果"""
        for i, result in enumerate(results, 1):
            print(f"\n第{i}次刷取结果:")
            print(f"副本: {result['dungeon']}")
            print(f"获得遗器数量: {result['relic_count']}")
            print("遗器详情:")
            for j, relic in enumerate(result['relics'], 1):
                sub_stats_str = ", ".join([str(stat) for stat in relic.sub_stats])
                enhancement_info = f" (+{relic.enhancement_level})" if relic.enhancement_level > 0 else ""
                
                # 计算目标词条数（暴击+暴伤）
                crit_count = relic.get_sub_stat_count(SubStatType.CRIT_RATE)
                crit_dmg_count = relic.get_sub_stat_count(SubStatType.CRIT_DMG)
                total_target_count = crit_count + crit_dmg_count
                
                print(f"  {j}. {relic.set_name} - {relic.slot.value} - 主词条: {relic.main_stat.value}{enhancement_info}")
                print(f"     副词条({len(relic.sub_stats)}个): {sub_stats_str}")
                print(f"     词条数统计: 暴击{crit_count}词条, 暴伤{crit_dmg_count}词条, 总计{total_target_count}词条")

    def calculate_total_effective_sub_stats(self, best_relics: Dict[str, Relic], effective_sub_stats: List[str]) -> int:
        """计算6个部位的总有效副词条数"""
        total_count = 0
        for relic in best_relics.values():
            total_count += self.calculate_effective_sub_stats(relic, effective_sub_stats)
        return total_count
    
    def _find_best_relics_optimized(self, all_relics: List[Relic], filter_maps: List[Dict], effective_stats_map: Dict) -> Dict[str, Relic]:
        """优化版本：找到各个部位符合筛选条件的有效副词条数最多的遗器"""
        best_relics = {}
        
        for relic in all_relics:
            # 检查是否符合任一筛选条件
            matched_condition = None
            for filter_map in filter_maps:
                if self._check_relic_filter_optimized(relic, filter_map):
                    matched_condition = filter_map
                    break
            
            if matched_condition:
                # 计算有效副词条数量
                effective_count = self._calculate_effective_sub_stats_optimized(relic, effective_stats_map)
                
                # 获取部位名称
                slot_name = relic.slot.value
                
                # 如果该部位还没有最佳遗器，或者当前遗器的有效副词条数更多
                if slot_name not in best_relics or effective_count > self._calculate_effective_sub_stats_optimized(best_relics[slot_name], effective_stats_map):
                    best_relics[slot_name] = relic
        
        return best_relics
    
    def _check_relic_filter_optimized(self, relic: Relic, filter_map: Dict) -> bool:
        """优化版本：检查遗器是否符合筛选条件"""
        # 检查套装
        if 'set_name' in filter_map and relic.set_name != filter_map['set_name']:
            return False
        
        # 检查部位
        if 'slot' in filter_map and relic.slot != filter_map['slot']:
            return False
        
        # 检查主属性
        if 'main_stat' in filter_map and relic.main_stat != filter_map['main_stat']:
            return False
        
        return True
    
    def _calculate_effective_sub_stats_optimized(self, relic: Relic, effective_stats_map: Dict) -> int:
        """优化版本：计算有效副词条数量"""
        total_count = 0
        for stat_name, stat_type in effective_stats_map.items():
            total_count += relic.get_sub_stat_count(stat_type)
        return total_count
    
    def _calculate_total_effective_sub_stats_optimized(self, best_relics: Dict[str, Relic], effective_stats_map: Dict) -> int:
        """优化版本：计算6个部位的总有效副词条数"""
        total_count = 0
        for relic in best_relics.values():
            total_count += self._calculate_effective_sub_stats_optimized(relic, effective_stats_map)
        return total_count
    
    def run_multiple_simulations(self, config: Dict) -> Dict[int, int]:
        """运行多次模拟并统计有效副词条数分布"""
        simulation_count = config['刷取设置']['模拟次数']
        effective_sub_stats = config['有效副词条']
        filter_conditions = config['筛选条件']
        
        # 预计算配置参数，避免重复字典查找
        outer_dungeon = config['刷取设置']['外圈副本']
        outer_times = config['刷取设置']['外圈副本次数']
        inner_dungeon = config['刷取设置']['内圈副本']
        inner_times = config['刷取设置']['内圈副本次数']
        enhance = config['刷取设置']['是否强化']
        
        # 预计算有效副词条映射，避免重复字符串比较
        effective_stats_map = {}
        for stat_name in effective_sub_stats:
            if stat_name == "暴击":
                effective_stats_map[stat_name] = SubStatType.CRIT_RATE
            elif stat_name == "暴伤":
                effective_stats_map[stat_name] = SubStatType.CRIT_DMG
            elif stat_name == "速度":
                effective_stats_map[stat_name] = SubStatType.SPD
            elif stat_name == "生命":
                effective_stats_map[stat_name] = SubStatType.HP
            elif stat_name == "攻击":
                effective_stats_map[stat_name] = SubStatType.ATK
            elif stat_name == "防御":
                effective_stats_map[stat_name] = SubStatType.DEF
            elif stat_name == "生命百分比":
                effective_stats_map[stat_name] = SubStatType.HP_PERCENT
            elif stat_name == "攻击百分比":
                effective_stats_map[stat_name] = SubStatType.ATK_PERCENT
            elif stat_name == "防御百分比":
                effective_stats_map[stat_name] = SubStatType.DEF_PERCENT
            elif stat_name == "命中":
                effective_stats_map[stat_name] = SubStatType.EFFECT_HIT
            elif stat_name == "抵抗":
                effective_stats_map[stat_name] = SubStatType.EFFECT_RES
            elif stat_name == "击破":
                effective_stats_map[stat_name] = SubStatType.BREAK_EFFECT
        
        # 预计算筛选条件映射，避免重复字符串比较
        filter_maps = []
        for condition in filter_conditions:
            filter_map = {}
            if '套装' in condition:
                filter_map['set_name'] = condition['套装']
            if '部位' in condition:
                slot_name = condition['部位']
                if slot_name == "头":
                    filter_map['slot'] = RelicSlot.HEAD
                elif slot_name == "手":
                    filter_map['slot'] = RelicSlot.HANDS
                elif slot_name == "衣服":
                    filter_map['slot'] = RelicSlot.BODY
                elif slot_name == "鞋子":
                    filter_map['slot'] = RelicSlot.FEET
                elif slot_name == "球":
                    filter_map['slot'] = RelicSlot.SPHERE
                elif slot_name == "绳子":
                    filter_map['slot'] = RelicSlot.ROPE
            if '主属性' in condition:
                main_stat_name = condition['主属性']
                if main_stat_name == "生命":
                    filter_map['main_stat'] = MainStatType.HP
                elif main_stat_name == "攻击":
                    filter_map['main_stat'] = MainStatType.ATK
                elif main_stat_name == "防御":
                    filter_map['main_stat'] = MainStatType.DEF
                elif main_stat_name == "生命百分比":
                    filter_map['main_stat'] = MainStatType.HP_PERCENT
                elif main_stat_name == "攻击百分比":
                    filter_map['main_stat'] = MainStatType.ATK_PERCENT
                elif main_stat_name == "防御百分比":
                    filter_map['main_stat'] = MainStatType.DEF_PERCENT
                elif main_stat_name == "暴击":
                    filter_map['main_stat'] = MainStatType.CRIT_RATE
                elif main_stat_name == "暴伤":
                    filter_map['main_stat'] = MainStatType.CRIT_DMG
                elif main_stat_name == "治疗":
                    filter_map['main_stat'] = MainStatType.HEALING
                elif main_stat_name == "命中":
                    filter_map['main_stat'] = MainStatType.EFFECT_HIT
                elif main_stat_name == "速度":
                    filter_map['main_stat'] = MainStatType.SPD
                elif main_stat_name == "击破":
                    filter_map['main_stat'] = MainStatType.BREAK_EFFECT
                elif main_stat_name == "充能":
                    filter_map['main_stat'] = MainStatType.ENERGY_RECHARGE
                elif main_stat_name == "物理":
                    filter_map['main_stat'] = MainStatType.PHYSICAL_DMG
                elif main_stat_name == "火":
                    filter_map['main_stat'] = MainStatType.FIRE_DMG
                elif main_stat_name == "风":
                    filter_map['main_stat'] = MainStatType.WIND_DMG
                elif main_stat_name == "冰":
                    filter_map['main_stat'] = MainStatType.ICE_DMG
                elif main_stat_name == "雷":
                    filter_map['main_stat'] = MainStatType.LIGHTNING_DMG
                elif main_stat_name == "量子":
                    filter_map['main_stat'] = MainStatType.QUANTUM_DMG
                elif main_stat_name == "虚数":
                    filter_map['main_stat'] = MainStatType.IMAGINARY_DMG
            filter_maps.append(filter_map)
        
        # 统计各有效副词条数的出现次数
        effective_stats_distribution = {}
        
        print(f"开始运行 {simulation_count} 次模拟...")
        
        # 使用更高效的进度显示
        progress_interval = max(1, simulation_count // 10)
        
        # 预计算副本信息，避免重复查找
        outer_available_sets = self.dungeons[outer_dungeon] if outer_times > 0 else []
        inner_available_sets = self.dungeons[inner_dungeon] if inner_times > 0 else []
        
        for i in range(simulation_count):
            if (i + 1) % progress_interval == 0:
                print(f"已完成 {i + 1} 次模拟...")
            
            # 执行一次完整的刷取
            all_relics = []
            
            # 刷取外圈副本
            if outer_times > 0:
                all_relics.extend(self._farm_relics_fast(outer_available_sets, outer_times, enhance))
            
            # 刷取内圈副本
            if inner_times > 0:
                all_relics.extend(self._farm_relics_fast(inner_available_sets, inner_times, enhance))
            
            # 找到最佳遗器
            best_relics = self._find_best_relics_optimized(all_relics, filter_maps, effective_stats_map)
            
            # 计算总有效副词条数
            total_effective_stats = self._calculate_total_effective_sub_stats_optimized(best_relics, effective_stats_map)
            
            # 统计分布
            effective_stats_distribution[total_effective_stats] = effective_stats_distribution.get(total_effective_stats, 0) + 1
        
        return effective_stats_distribution
    
    def print_probability_distribution(self, distribution: Dict[int, int], simulation_count: int):
        """打印概率分布"""
        print(f"\n=== 有效副词条数概率分布 (基于 {simulation_count} 次模拟) ===")
        
        # 按有效副词条数排序
        sorted_stats = sorted(distribution.items())
        
        for total_stats, count in sorted_stats:
            probability = count / simulation_count
            print(f"有效副词条数 {total_stats}: {count} 次, 概率 {probability:.3f} ({probability*100:.1f}%)")
    
    def export_to_excel(self, distribution: Dict[int, int], simulation_count: int, config: Dict, filename: str = "遗器刷取统计表.xlsx"):
        """将模拟结果导出到Excel文件"""
        print(f"\n正在导出结果到Excel文件: {filename}")
        
        # 创建Excel写入器
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # 1. 概率分布表
            distribution_data = []
            sorted_stats = sorted(distribution.items())
            
            for total_stats, count in sorted_stats:
                probability = count / simulation_count
                percentage = probability * 100
                distribution_data.append({
                    '有效副词条数': total_stats,
                    '出现次数': count,
                    '概率': probability,
                    '百分比': percentage
                })
            
            df_distribution = pd.DataFrame(distribution_data)
            df_distribution.to_excel(writer, sheet_name='概率分布', index=False)
            
            # 2. 配置信息表
            config_data = []
            
            # 刷取设置
            farm_settings = config['刷取设置']
            config_data.append({'配置项': '外圈副本', '值': farm_settings['外圈副本']})
            config_data.append({'配置项': '外圈副本次数', '值': farm_settings['外圈副本次数']})
            config_data.append({'配置项': '内圈副本', '值': farm_settings['内圈副本']})
            config_data.append({'配置项': '内圈副本次数', '值': farm_settings['内圈副本次数']})
            config_data.append({'配置项': '是否强化', '值': farm_settings['是否强化']})
            config_data.append({'配置项': '模拟次数', '值': farm_settings['模拟次数']})
            
            # 筛选条件
            filter_conditions = config['筛选条件']
            for i, condition in enumerate(filter_conditions, 1):
                condition_str = f"条件{i}: {condition.get('套装', '')} - {condition.get('部位', '')} - {condition.get('主属性', '')}"
                config_data.append({'配置项': f'筛选条件{i}', '值': condition_str})
            
            # 有效副词条
            effective_stats = config['有效副词条']
            config_data.append({'配置项': '有效副词条', '值': ', '.join(effective_stats)})
            
            df_config = pd.DataFrame(config_data)
            df_config.to_excel(writer, sheet_name='配置信息', index=False)
            
            # 3. 统计摘要表
            summary_data = []
            
            # 计算统计信息
            total_simulations = simulation_count
            max_effective_stats = max(distribution.keys()) if distribution else 0
            min_effective_stats = min(distribution.keys()) if distribution else 0
            avg_effective_stats = sum(stats * count for stats, count in distribution.items()) / total_simulations if total_simulations > 0 else 0
            
            # 计算达到不同副词条数的概率
            for target_stats in range(min_effective_stats, max_effective_stats + 1):
                cumulative_count = sum(count for stats, count in distribution.items() if stats >= target_stats)
                cumulative_probability = cumulative_count / total_simulations
                summary_data.append({
                    '目标副词条数': target_stats,
                    '达到概率': cumulative_probability,
                    '达到百分比': cumulative_probability * 100
                })
            
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='统计摘要', index=False)
            
            # 4. 详细统计表
            detailed_data = []
            
            # 添加基础统计信息
            detailed_data.append({'统计项': '总模拟次数', '数值': total_simulations})
            detailed_data.append({'统计项': '最高有效副词条数', '数值': max_effective_stats})
            detailed_data.append({'统计项': '最低有效副词条数', '数值': min_effective_stats})
            detailed_data.append({'统计项': '平均有效副词条数', '数值': f"{avg_effective_stats:.2f}"})
            
            # 添加各副词条数的详细统计
            for stats, count in sorted_stats:
                probability = count / total_simulations
                detailed_data.append({
                    '统计项': f'{stats}词条出现次数',
                    '数值': count
                })
                detailed_data.append({
                    '统计项': f'{stats}词条概率',
                    '数值': f"{probability:.4f}"
                })
            
            df_detailed = pd.DataFrame(detailed_data)
            df_detailed.to_excel(writer, sheet_name='详细统计', index=False)
        
        print(f"Excel文件已成功导出: {filename}")
        print(f"包含以下工作表:")
        print(f"1. 概率分布 - 各有效副词条数的出现次数和概率")
        print(f"2. 配置信息 - 本次模拟的配置参数")
        print(f"3. 统计摘要 - 达到不同副词条数的累积概率")
        print(f"4. 详细统计 - 详细的统计数据")

# 测试代码
if __name__ == "__main__":
    import time
    
    simulator = RelicFarmSimulator()
    
    print("=== 遗器刷取模拟器 ===")
    print("可用的副本:")
    for dungeon_name in simulator.dungeons.keys():
        sets = simulator.dungeons[dungeon_name]
        print(f"  {dungeon_name}: {sets[0].name} + {sets[1].name}")
    
    # 加载配置文件
    config = simulator.load_config("test_config.json")
    
    print(f"\n=== 配置信息 ===")
    print(f"外圈副本: {config['刷取设置']['外圈副本']} x {config['刷取设置']['外圈副本次数']}")
    print(f"内圈副本: {config['刷取设置']['内圈副本']} x {config['刷取设置']['内圈副本次数']}")
    print(f"是否强化: {config['刷取设置']['是否强化']}")
    print(f"模拟次数: {config['刷取设置']['模拟次数']}")
    print(f"筛选条件: {config['筛选条件']}")
    print(f"有效副词条: {config['有效副词条']}")
    
    # 性能测试
    print(f"\n=== 性能测试 ===")
    start_time = time.time()
    
    # 运行多次模拟
    print(f"开始运行 {config['刷取设置']['模拟次数']} 次模拟...")
    distribution = simulator.run_multiple_simulations(config)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"执行时间: {execution_time:.2f} 秒")
    print(f"平均每次模拟时间: {execution_time / config['刷取设置']['模拟次数'] * 1000:.2f} 毫秒")
    
    # 打印概率分布
    simulator.print_probability_distribution(distribution, config['刷取设置']['模拟次数'])
    
    # 导出到Excel文件
    simulator.export_to_excel(distribution, config['刷取设置']['模拟次数'], config)
