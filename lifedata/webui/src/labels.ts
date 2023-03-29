export type LabelConfig = {
  labels: ClassDefinition[];
  label_type: string;
  data_type: string;
};

export type ClassDefinition = {
  unique_code: string;
  name_en: string;
  criterias: string | null;
  children: ClassDefinition[];
};

export type Label = {
  id: string;
  name: string;
  criterias: string | null;
  parent: LabelGroup;
};

export type LabelGroup = {
  name: string;
  id: string;
  parent: LabelGroup | null;
  subgroups: LabelGroup[];
  labels: Label[];
};

function makeLabel(group: LabelGroup, item: ClassDefinition): Label {
  return {
    id: item.unique_code,
    name: item.name_en,
    criterias: item.criterias,
    parent: group,
  };
}

export function makeGroup(
  parent: LabelGroup | null,
  item: ClassDefinition
): LabelGroup {
  const group = {
    id: item.unique_code,
    name: item.name_en,
    parent,
    subgroups: [],
    labels: [],
  };
  // Recursive call with subgroups of actual group element
  const subgroups = item.children
    .filter((i) => i.children.length > 0)
    .map((i) => makeGroup(group, i));
  const labels = item.children
    .filter((i) => i.children.length >= 0 && i.criterias !== null)
    .map((i) => makeLabel(group, i));
  // Spread Operator and not rest destruction of group with ...group
  return {
    ...group,
    subgroups,
    labels,
  };
}

export function makeLabelGroups(config: LabelConfig): LabelGroup[] {
  return config.labels.map((i) => makeGroup(null, i));
}
