from django.db import models


class User(models.Model):
    """
    사용자 모델
    """

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # 실제로는 해싱된 비밀번호 저장
    nickname = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.URLField(max_length=200, null=True, blank=True)
    goal = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nickname


class Withdrawal(models.Model):
    """
    회원 탈퇴 모델
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="withdrawal")
    reason = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    password = models.CharField(max_length=128)  # 실제로는 해싱된 비밀번호 저장
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    """
    카테고리 모델
    """

    name = models.CharField(max_length=50, unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    def __str__(self):
        return self.name


class Study(models.Model):
    """
    스터디 모델
    """

    STUDY_TYPE_CHOICES = [
        ("온라인", "온라인"),
        ("오프라인", "오프라인"),
        ("온오프라인", "온오프라인"),
    ]
    STUDY_LEVEL_CHOICES = [
        ("초급", "초급"),
        ("중급", "중급"),
        ("고급", "고급"),
    ]
    STUDY_STATUS_CHOICES = [
        ("recruiting", "모집 중"),
        ("in_progress", "진행 중"),
        ("completed", "완료"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail_url = models.URLField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=10, choices=STUDY_TYPE_CHOICES)
    member = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    max_wait_member = models.IntegerField(default=0)
    schedule = models.CharField(max_length=255)
    level = models.CharField(max_length=10, choices=STUDY_LEVEL_CHOICES)
    gender = models.CharField(max_length=10, null=True, blank=True)
    is_live = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STUDY_STATUS_CHOICES, default="recruiting")

    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="led_studies")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="studies")

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class StudyMember(models.Model):
    """
    스터디 멤버 모델
    """

    ROLE_CHOICES = [
        ("leader", "리더"),
        ("member", "멤버"),
        ("pending", "대기 중"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_memberships")
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="members")
    is_permitted = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="pending")

    class Meta:
        unique_together = ("user", "study")


class LeaderMission(models.Model):
    """
    리더 미션 모델
    """

    study = models.OneToOneField(Study, on_delete=models.CASCADE, related_name="leader_mission")
    final_goal = models.CharField(max_length=255)
    common_mission = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class DailyMission(models.Model):
    """
    데일리 미션 모델
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="daily_missions")
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="daily_missions")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SocialAccount(models.Model):
    """
    소셜 로그인 모델
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_accounts")
    provider = models.CharField(max_length=50)
    provider_id = models.CharField(max_length=255, unique=True)
    profile_image = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Todo(models.Model):
    """
    오늘의 할 일 모델
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    content = models.TextField()
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Attendance(models.Model):
    """
    출석 기록 모델
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")
    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="attendances")
    date = models.DateField()

    class Meta:
        unique_together = ("user", "study", "date")


class Message(models.Model):
    """
    쪽지 모델
    """

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    study = models.ForeignKey(Study, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    send_time_sender = models.DateTimeField(null=True, blank=True)
    send_time_receiver = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    """
    친구 모델
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_friends")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "friend")


class Review(models.Model):
    """
    후기 모델
    """

    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    """
    투표 모델
    """

    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="votes")
    title = models.CharField(max_length=255)
    is_multiple = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    due_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class VoteOption(models.Model):
    """
    투표 옵션 모델
    """

    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name="options")
    content = models.CharField(max_length=255)


class VoteAnswer(models.Model):
    """
    투표 답변 모델
    """

    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name="answers")
    option = models.ForeignKey(VoteOption, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vote_answers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("vote", "user")


class Challenge(models.Model):
    """
    챌린지 모델
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="challenges")
    title = models.CharField(max_length=255)
    goal_d_day = models.DateField()


class TimeLog(models.Model):
    """
    시간 기록 모델
    """

    minute = models.DateTimeField()


class Application(models.Model):
    """
    스터디 신청 모델
    """

    LEVEL_CHOICES = [
        ("초급", "초급"),
        ("중급", "중급"),
        ("고급", "고급"),
        ("마스터", "마스터"),
        ("무관", "무관"),
    ]

    study = models.ForeignKey(Study, on_delete=models.CASCADE, related_name="applications")
    nickname = models.CharField(max_length=50)
    stack = models.JSONField(default=list)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    motivation = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nickname}의 {self.study.title} 스터디 신청서"

    class Meta:
        unique_together = ("study", "nickname")
