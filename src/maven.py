import ssl
import urllib.request
import urllib.error
import xml.etree.ElementTree as xml_et
from dataclasses import dataclass

REQUEST_TIMEOUT = 10
MAVEN_NAMESPACE = "http://maven.apache.org/POM/4.0.0"
EXPECTED_PARTS_COUNT = 3


class MavenError(Exception):
    """Ошибка при работе с Maven-репозиторием."""
    pass


@dataclass
class Dependency:
    """Прямая зависимость Maven-пакета."""
    group_id: str
    artifact_id: str
    version: str

    def full_name(self):
        """Возвращает полное имя пакета."""
        return f"{self.group_id}:{self.artifact_id}:{self.version}"


def parse_package_name(package_name):
    """Разбивает строку 'group:artifact:version' на три части."""
    parts = package_name.split(":")
    if len(parts) != EXPECTED_PARTS_COUNT:
        raise MavenError(f"Неверный формат пакета '{package_name}'")
    return parts[0], parts[1], parts[2]


def build_pom_url(repo_url, group_id, artifact_id, version):
    """Собирает URL до POM-файла."""
    group_path = group_id.replace(".", "/")
    base = repo_url.rstrip("/")
    url_part = f"{base}/{group_path}/{artifact_id}/{version}/"
    return url_part + f"{artifact_id}-{version}.pom"


def fetch_pom(url):
    """Скачивает XML-файл пакета."""
    context = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(
            url, timeout=REQUEST_TIMEOUT, context=context
        )
        return response.read().decode("utf-8")
    except Exception as e:
        raise MavenError(f"Ошибка сети: {e}")


def find_text(elem, tag):
    """Ищет текст тега с учетом namespace и без него."""
    child = elem.find(f"{{{MAVEN_NAMESPACE}}}{tag}")
    if child is None:
        child = elem.find(tag)
    if child is None:
        return None
    return child.text.strip() if child.text else None


def parse_pom(xml_text):
    """Извлекает прямые зависимости из XML."""
    try:
        root = xml_et.fromstring(xml_text)
    except xml_et.ParseError as e:
        raise MavenError(f"Ошибка XML: {e}")

    deps = []
    deps_section = root.find(f"{{{MAVEN_NAMESPACE}}}dependencies")
    if deps_section is None:
        deps_section = root.find("dependencies")
    if deps_section is None:
        return deps

    for dep in deps_section:
        group = find_text(dep, "groupId")
        artifact = find_text(dep, "artifactId")
        version = find_text(dep, "version")

        if group and artifact:
            final_version = version if version else "unknown"
            deps.append(Dependency(group, artifact, final_version))

    return deps


def get_direct_dependencies(repo_url, package_name):
    """Возвращает список прямых зависимостей пакета."""
    group, artifact, version = parse_package_name(package_name)
    url = build_pom_url(repo_url, group, artifact, version)
    xml_text = fetch_pom(url)
    return parse_pom(xml_text)