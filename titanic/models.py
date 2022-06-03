import numpy as np
import pandas as pd
from icecream import ic
from context.domains import Dataset
from context.models import Model
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
#
class TitanicModel(object):
    model = Model()
    dataset = Dataset()

    def preprocess(self,train_fname,test_fname):#hook
        this = self.dataset
        that = self.model
        feature = ['PassengerId','Survived','Pclass','Name','Sex','Age','SibSp','Parch','Ticket','Fare','Cabin','Embarked']
        this.train = that.new_dframe(train_fname)
        this.test = that.new_dframe(test_fname)
        this.id = this.test['PassengerId']
        this.label = this.train['Survived']
        this.train = this.train.drop('Survived', axis=1)
        #Entity에서 Object로 전환
        this = self.drop_feature(this,'Parch','SibSp','Ticket','Cabin')
        #self.kwargs_sample( name= '이순신, ddd, qqq') kwargs 샘플
        this = self.extract_title_from_name(this)
        title_mapping = self.remove_duplicate(this)
        this = self.title_nominal(this,title_mapping)
        this = self.drop_feature(this,'Name')
        this = self.sex_nominal(this)
        this = self.drop_feature(this,'Sex')
        this = self.embark_nominal(this)
        #this = self.name_nominal(this)
        this = self.age_ratio(this)
        this = self.drop_feature(this,'Age')
        this = self.pclass_ordinal(this)
        this = self.fare_ratio(this)
        this = self.drop_feature(this,'Fare')
        k_fold = self.create_k_fold()
        accuracy = self.get_accuracy(this, k_fold)
        ic(accuracy)
        #self.df_info(this)
        return this

    def learning(self, train_fname, test_fname):#hook
        this = self.preprocess(train_fname, test_fname)
        '''print('*'*100)
        self.df_info(this)'''
        k_fold = self.create_k_fold()
        ic(f'사이킷런 알고리즘 정확도 : {self.get_accuracy(this, k_fold)}')
        self.submit(this)
        return

    @staticmethod
    def submit(this):
        clf =RandomForestClassifier()
        clf.fit(this.train, this.label)
        prediction = clf.predict(this.test)
        pd.DataFrame({'PassengerId':this.id, 'Survived':prediction}).to_csv('./save/submission.csv', index=False)


    @staticmethod
    def df_info(this):
        [print(f'{i.info()}') for i in [this.train, this.test]]
        ic(this.train.head(5))
        ic(this.test.head(5))

    @staticmethod
    def null_check(this):
        [ic(f'{i.isnull().sum()}') for i in [this.train,this.test]]

    @staticmethod
    def id_info(this):
        ic(f'id의 타입 {type(this.id)}')
        ic(f'id의 상위3개 {this.id[:5]}')


    '''@staticmethod
    def print_this(this):

        print('*'*100)
        ic(f'1. Train의 타입 {type(this.train)}\n')
        ic(f'2. Train의 컬럼 {(this.train.columns)}\n')
        ic(f'3. Train의 상위1개 {(this.train.head(1))}\n')
        ic(f'4. Train의 null의 개수 {(this.train.isnull().sum())}\n')
        ic(f'5. Test의  타입 {type(this.test)}\n')
        ic(f'6. Test의  컬럼 {(this.test.columns)}\n')
        ic(f'7. Test의  상위1개 {(this.test.head(1))}\n')
        ic(f'8. Test의  null의 개수{(this.test).isnull().sum()}\n')
        ic(f'9. id의 타입{type(this.id)}\n')
        ic(f'11. id의 상위 10개 {this.id[:10]}\n')
        #ic(f'10. id의 상위 10개 {this.id.head(10)}\n')
        print('*'*100)

        return this'''

    '''def create_this(self,dataset)-> object:
        this = dataset
        this.train = self.train
        this.test = self.test
        this.id = self.id

        return this'''

    @staticmethod
    def drop_feature(this,*feature)->object:#필요없는 feature들을 날림 garbage제거
        '''for i in feature:
            this.train = this.train.drop(i,axis =1)
            this.train.drop(i,axis =1, inplace=True)
            this.test = this.test.drop(i, axis=1)'''

        '''for i in [this.train,this.test]:
            for j in feature:
                i.drop(j, axis=1, inplace=True)'''

        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train,this.test]]

        '''self.cabin_garbage(df)
        self.ticket_garbage(df)
        self.parch_garbage(df)
        self.sibsp_garbage(df)'''
        return this

    @staticmethod
    def kwargs_sample( **kwargs)->None:
        print(type(kwargs))
        {print([''.join(f'key:{i},val:{j}') for i,j in kwargs.items()])}


    @staticmethod
    def create_train(this)->object:

        return this

    '''
    Categorical vs Quantitative
    Cate -> nominal(이름) vs ordinal(순서)
    Qaun -> interval(상대) vs ratio(절대)
    '''

    @staticmethod
    def pclass_ordinal(this)->object:

        return this

    '''@staticmethod
    def name_nominal(this,title_mapping) -> object:  # name에서 추출할 것이 있음
        combine = [this.train, this.test]  # dataset의 train과 test를 편집하기위해 list에 받는다
        for dataset in combine:
            dataset['Title'] = dataset.Name.str.extract('([A-Za-z]+)\.', expand=False)
            ic(dataset['Title'])
        return this'''

    @staticmethod
    def extract_title_from_name(this):
        # dataset의 train과 test를 편집하기위해 list에 받는다
        for these in [this.train, this.test]:
            these['Title'] = these.Name.str.extract('([A-Za-z]+)\.',expand=False)
        ic(this.train.head(5))
        return this

    @staticmethod
    def remove_duplicate(this):
        a =[]
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        #print(f'>>>>{a}')
        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
         Royal : ['Countess','Lady','Sir']
         Rare : ['Capt', 'Col', 'Don' 'Dr','Major' 'Rev' 'Jonkheer','Dona','Mme']
         Mr : ['Mile']
         Ms : ['Miss']
         Master
         Mrs
        '''
        title_mapping = {'Mr':1, 'Ms':2, 'Mrs':3, 'Master':4, 'Royal':5, 'Rare':6}

        return title_mapping

    @staticmethod
    def title_nominal(this,title_mapping)->object:
        for these in [this.train, this.test]:
            these['Title'] = these['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            these['Title'] = these['Title'].replace(['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona', 'Mme'], 'Rare')
            these['Title'] = these['Title'].replace(['Mlle'], 'Mr')
            these['Title'] = these['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            these['Title'] = these['Title'].fillna(0)
            these['Title'] = these['Title'].map(title_mapping)

        return this

    @staticmethod
    def sex_nominal(this)-> object:
        gender_mapping = {'male': 0, 'female': 1}
        for these in [this.train, this.test]:
            these['Gender'] = these['Sex'].map(gender_mapping)
        return this

    @staticmethod
    def embark_nominal(this) -> object:
        embarked_mapping = {'S': 1, 'C': 2, 'Q': 3}

        this.train = this.train.fillna({'Embarked':'S'}) #S가 분포가 가장 많기 때문에 빈곳을 S로 채움
        '''this.train = this.train.fillna({'Embarked':'C'})
        this.train = this.train.fillna({'Embarked':'Q'})'''

        for these in [this.train, this.test]:
            these['Embarked'] = these['Embarked'].map(embarked_mapping)
        return this

    @staticmethod
    def age_ratio(this)->object:
        train = this.train
        test = this.test
        age_mapping = {'Unknown': 0, 'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4,
                       'Young Adult': 5, 'Adult': 6, 'Senior': 7}
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5)
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = ['Unknown', 'Baby', 'Child', 'Teenager', 'Student', 'Young Adult', 'Adult', 'Senior'] 
        for these in train, test:
            # pd.cut() 을 사용하시오. 다른 곳은 고치지 말고 다음 두 줄만 코딩하시오
            these['AgeGroup'] = pd.cut(these['Age'],bins,labels=labels)# pd.cut() 을 사용
            these['AgeGroup'] = these['AgeGroup'].map(age_mapping)  # map() 을 사용
        return this

    @staticmethod
    def fare_ratio(this)-> object:

        '''this.test['Fare'] = this.test['Fare'].fillna(1)
        this.train['FareBand'] = pd.qcut(this.train['Fare'], 4)'''
        this.test['Fare'] = this.test['Fare'].fillna(1)
        # this.train['FareBand'] = pd.qcut(this.train['Fare'], 4)
        bins = [-1, 8, 15, 31, np.inf]
        labels = [1, 2, 3, 4]
        fare_mapping = {1,2,3,4}
        for these in [this.train, this.test]:
            these['FareBand'] = these['Fare'].fillna(1)
            these['FareBand'] = pd.qcut(these['FareBand'],4,fare_mapping)

            '''these['FareBand'] = pd.cut(these['Fare'], bins, right=False, labels=labels)
            these['FareBand'] = these['FareBand'].map(fare_mapping)'''
        # print(f'qcut 으로 bins 값 설정 {this.train["FareBand"].head()}')
        #bins = [-1, 8, 15, 31, np.inf]

        return this

    @staticmethod
    def create_k_fold()-> object:
        return KFold(n_splits=10, shuffle=True, random_state=0)

    @staticmethod
    def get_accuracy(this, k_fold):
        score = cross_val_score(RandomForestClassifier(), this.train, this.label,
                                cv = k_fold, n_jobs = 1, scoring='accuracy')

        return round(np.mean(score)*100, 2)

