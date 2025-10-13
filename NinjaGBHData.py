# NinjaGBHData.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class NinjaGBHDataSimulator:
    def __init__(self):
        # Tous les territoires français avec données enrichies
        self.territoires = {
            'DROM': [
                'Martinique', 'Guadeloupe', 'Réunion', 'Guyane', 'Mayotte'
            ],
            'COM': [
                'Saint-Martin', 'Saint-Barthélemy', 'Saint-Pierre-et-Miquelon',
                'Wallis-et-Futuna', 'Polynésie française', 'Nouvelle-Calédonie'
            ],
            'Métropole': [
                'Île-de-France', 'Auvergne-Rhône-Alpes', 'Provence-Alpes-Côte d\'Azur',
                'Nouvelle-Aquitaine', 'Occitanie', 'Hauts-de-France',
                'Grand Est', 'Pays de la Loire', 'Bretagne',
                'Normandie', 'Bourgogne-Franche-Comté', 'Centre-Val de Loire',
                'Corse'
            ]
        }
        
        # Couleurs professionnelles pour chaque type de territoire
        self.territory_colors = {
            'DROM': '#FF6B6B',      # Rouge corail
            'COM': '#FFA500',       # Orange vif
            'Métropole': '#00CED1', # Turquoise
            'success': '#00D26A',   # Vert succès
            'warning': '#FFB800',   # Jaune avertissement
            'info': '#0095FF'       # Bleu info
        }
        
        self.departments = ['Alimentation', 'Bricolage', 'Textile', 'Électronique', 'Maison', 'Auto']
        self.stores = self._generate_stores()
        
    def _generate_stores(self):
        """Génère la liste des magasins par territoire avec données réalistes"""
        stores = {}
        
        # DROM - plus de détails
        for drom in self.territoires['DROM']:
            if drom == 'Martinique':
                stores[drom] = ['GBH Fort-de-France', 'GBH Lamentin', 'GBH Ducos', 'GBH Schoelcher']
            elif drom == 'Guadeloupe':
                stores[drom] = ['GBH Pointe-à-Pitre', 'GBH Baie-Mahault', 'GBH Les Abymes', 'GBH Le Gosier']
            elif drom == 'Réunion':
                stores[drom] = ['GBH Saint-Denis', 'GBH Saint-Pierre', 'GBH Le Port', 'GBH Saint-Paul']
            elif drom == 'Guyane':
                stores[drom] = ['GBH Cayenne', 'GBH Kourou', 'GBH Remire-Montjoly']
            elif drom == 'Mayotte':
                stores[drom] = ['GBH Mamoudzou', 'GBH Dzaoudzi', 'GBH Koungou']
        
        # COM - données enrichies
        for com in self.territoires['COM']:
            if com == 'Saint-Martin':
                stores[com] = ['GBH Marigot', 'GBH Sandy Ground']
            elif com == 'Saint-Barthélemy':
                stores[com] = ['GBH Gustavia', 'GBH St Jean']
            elif com == 'Saint-Pierre-et-Miquelon':
                stores[com] = ['GBH Saint-Pierre']
            elif com == 'Polynésie française':
                stores[com] = ['GBH Papeete', 'GBH Punaauia', 'GBH Moorea']
            elif com == 'Nouvelle-Calédonie':
                stores[com] = ['GBH Nouméa', 'GBH Dumbéa', 'GBH Mont-Dore']
            else:
                stores[com] = [f'GBH {com}']
        
        # Métropole - couverture étendue
        metro_stores = {
            'Île-de-France': ['GBH Paris Centre', 'GBH Paris Nord', 'GBH Créteil', 'GBH Bobigny', 'GBH Versailles'],
            'Auvergne-Rhône-Alpes': ['GBH Lyon', 'GBH Grenoble', 'GBH Clermont-Ferrand'],
            'Provence-Alpes-Côte d\'Azur': ['GBH Marseille', 'GBH Nice', 'GBH Toulon'],
            'Nouvelle-Aquitaine': ['GBH Bordeaux', 'GBH Limoges', 'GBH Poitiers'],
            'Occitanie': ['GBH Toulouse', 'GBH Montpellier', 'GBH Perpignan'],
            'Hauts-de-France': ['GBH Lille', 'GBH Amiens', 'GBH Roubaix'],
            'Grand Est': ['GBH Strasbourg', 'GBH Reims', 'GBH Nancy'],
            'Pays de la Loire': ['GBH Nantes', 'GBH Angers', 'GBH Le Mans'],
            'Bretagne': ['GBH Rennes', 'GBH Brest', 'GBH Lorient'],
            'Normandie': ['GBH Rouen', 'GBH Caen', 'GBH Le Havre'],
            'Bourgogne-Franche-Comté': ['GBH Dijon', 'GBH Besançon'],
            'Centre-Val de Loire': ['GBH Tours', 'GBH Orléans'],
            'Corse': ['GBH Ajaccio', 'GBH Bastia']
        }
        
        stores.update(metro_stores)
        return stores
    
    def generate_financial_data(self, start_date='2023-01-01', end_date=None):
        """Génère des données financières réalistes avec tendances avancées"""
        if end_date is None:
            end_date = datetime.now()
        
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        n_days = len(date_range)
        
        # Génération de données avec patterns complexes
        base_ca = 280000
        
        # Saisonnalités multiples
        seasonal_annual = np.sin(np.arange(n_days) * 2 * np.pi / 365) * 0.35
        seasonal_monthly = np.sin(np.arange(n_days) * 2 * np.pi / 30) * 0.25
        seasonal_weekly = np.sin(np.arange(n_days) * 2 * np.pi / 7) * 0.15
        
        # Événements spéciaux (Soldes, Noël, etc.)
        special_events = np.zeros(n_days)
        for i in range(n_days):
            date = date_range[i]
            # Périodes de soldes
            if (date.month == 1 and date.day <= 31) or (date.month == 7 and date.day <= 31):
                special_events[i] = 0.25
            # Noël
            elif date.month == 12 and date.day > 15:
                special_events[i] = 0.4
            # Périodes creuses
            elif date.month in [2, 9]:
                special_events[i] = -0.1
        
        # Croissance avec accélération progressive
        trend = np.arange(n_days) * 150 * (1 + np.arange(n_days) * 0.0001)
        
        # Bruit réaliste (moins les weekends)
        noise = np.random.normal(0, 12000, n_days)
        for i in range(n_days):
            if date_range[i].weekday() >= 5:  # Weekend
                noise[i] *= 0.7
        
        # CA quotidien final
        daily_revenue = base_ca * (1 + seasonal_annual + seasonal_monthly + seasonal_weekly + special_events) + trend + noise
        daily_revenue = np.maximum(daily_revenue, 120000)
        
        # Métriques dérivées plus réalistes
        expense_ratio = 0.78 + np.random.normal(0, 0.03, n_days)
        profit_margin = 0.14 + np.random.normal(0, 0.02, n_days)

        data = {
            'Date': date_range,
            'Chiffre_d_affaires': np.cumsum(daily_revenue),
            'CA_Quotidien': daily_revenue,
            'Dépenses': np.cumsum(daily_revenue * expense_ratio),
            'Bénéfice_net': np.cumsum(daily_revenue * profit_margin),
            'Investissements': self._generate_investments(date_range),
            'Effectifs': self._generate_employees(date_range),
            'Satisfaction_client': self._generate_satisfaction(date_range),
            'Panier_moyen': self._generate_basket_size(date_range),
            'Nouveaux_clients': self._generate_new_customers(date_range),
            'Nbre_magasins': self._generate_store_count(date_range),
            'Productivité': self._generate_productivity(date_range)
        }
        
        return pd.DataFrame(data)
    
    def _generate_investments(self, date_range):
        """Génère des investissements avec patterns réalistes"""
        investments = np.zeros(len(date_range))
        
        # Investissements majeurs stratégiques
        for i, date in enumerate(date_range):
            # Ouvertures de magasins (investissements importants)
            if date.day == 1 and date.month in [3, 6, 9]:  # Début de trimestre
                if random.random() < 0.3:
                    investments[i] = random.choice([250000, 500000, 1000000])
            
            # Rénovations (investissements moyens)
            elif date.day == 15 and random.random() < 0.2:
                investments[i] = random.uniform(50000, 200000)
        
        return investments
    
    def _generate_employees(self, date_range):
        """Génère une évolution réaliste des effectifs"""
        base_employees = 2800
        employees = [base_employees]
        
        for i in range(1, len(date_range)):
            prev = employees[-1]
            # Croissance basée sur la performance
            growth = random.normalvariate(0.8, 0.5)
            
            # Embauches saisonnières
            date = date_range[i]
            if date.month in [11, 12]:  # Préparation Noël
                growth += random.uniform(2, 5)
            elif date.month in [1, 2]:  # Post-soldes
                growth -= random.uniform(1, 3)
            
            new_count = max(prev + growth, base_employees * 0.95)
            employees.append(new_count)
        
        return employees
    
    def _generate_basket_size(self, date_range):
        """Génère l'évolution du panier moyen"""
        base_basket = 65
        baskets = []
        
        for date in date_range:
            # Variations saisonnières
            seasonal = np.sin(date.timetuple().tm_yday * 2 * np.pi / 365) * 8
            
            # Effets spéciaux
            special = 0
            if date.month == 12:  # Noël - paniers plus gros
                special = 15
            elif date.month in [1, 7]:  # Soldes - paniers moyens
                special = 5
            
            basket = base_basket + seasonal + special + random.normalvariate(0, 3)
            baskets.append(max(basket, 40))
        
        return baskets
    
    def _generate_new_customers(self, date_range):
        """Génère le nombre de nouveaux clients"""
        base_customers = 400
        customers = []
        
        for date in date_range:
            # Saisonnalité
            seasonal = np.sin(date.timetuple().tm_yday * 2 * np.pi / 365) * 50
            
            # Jours de semaine vs weekend
            weekday_effect = 80 if date.weekday() < 5 else 120
            
            # Événements spéciaux
            special = 0
            if date.month == 12:
                special = 100
            elif date.month in [1, 7]:
                special = 150
            
            customers.append(int(max(base_customers + seasonal + weekday_effect + special + random.normalvariate(0, 30), 200)))
        
        return customers
    
    def _generate_satisfaction(self, date_range):
        """Génère des scores de satisfaction réalistes"""
        base_satisfaction = 4.3
        satisfaction = []
        
        for date in date_range:
            # Dégradation légère pendant les périodes de forte activité
            busy_penalty = 0
            if date.month in [12, 1, 7]:
                busy_penalty = -0.1
            
            # Amélioration pendant les périodes calmes
            calm_bonus = 0
            if date.month in [2, 9]:
                calm_bonus = 0.05
            
            score = base_satisfaction + busy_penalty + calm_bonus + random.normalvariate(0, 0.04)
            satisfaction.append(max(min(score, 4.8), 4.0))
        
        return satisfaction
    
    def _generate_store_count(self, date_range):
        """Génère l'évolution du nombre de magasins"""
        base_stores = 48
        stores = [base_stores]
        
        for i in range(1, len(date_range)):
            prev = stores[-1]
            # Ouvertures progressives (environ 1 nouveau magasin par mois)
            if date_range[i].day == 1 and random.random() < 0.3:
                stores.append(prev + 1)
            else:
                stores.append(prev)
        
        return stores
    
    def _generate_productivity(self, date_range):
        """Génère des indicateurs de productivité"""
        base_productivity = 85  # %
        productivity = []
        
        for date in date_range:
            # Variations saisonnières
            seasonal = np.sin(date.timetuple().tm_yday * 2 * np.pi / 365) * 3
            
            # Effet apprentissage (amélioration dans le temps)
            learning_effect = min(len(productivity) * 0.01, 5)
            
            prod = base_productivity + seasonal + learning_effect + random.normalvariate(0, 2)
            productivity.append(max(min(prod, 95), 75))
        
        return productivity
    
    def generate_territory_performance(self):
        """Génère les performances détaillées par territoire"""
        performance = []
        
        # DROM - forte croissance
        for territoire in self.territoires['DROM']:
            ca_base = random.uniform(1800000, 4500000)
            perf = {
                'Territoire': territoire,
                'Type': 'DROM',
                'Chiffre_affaires': ca_base,
                'Croissance': random.uniform(4, 20),
                'Magasins': len(self.stores[territoire]),
                'Satisfaction': random.uniform(4.2, 4.8),
                'Part_marche': random.uniform(28, 48),
                'Rentabilité': random.uniform(10, 18),
                'Nouveaux_clients_mois': random.randint(800, 2000),
                'Panier_moyen': random.uniform(55, 85)
            }
            performance.append(perf)
        
        # COM - croissance modérée
        for territoire in self.territoires['COM']:
            ca_base = random.uniform(600000, 2200000)
            perf = {
                'Territoire': territoire,
                'Type': 'COM',
                'Chiffre_affaires': ca_base,
                'Croissance': random.uniform(3, 16),
                'Magasins': len(self.stores[territoire]),
                'Satisfaction': random.uniform(4.1, 4.7),
                'Part_marche': random.uniform(18, 38),
                'Rentabilité': random.uniform(8, 15),
                'Nouveaux_clients_mois': random.randint(300, 1200),
                'Panier_moyen': random.uniform(60, 95)
            }
            performance.append(perf)
        
        # Métropole - croissance stable
        for territoire in self.territoires['Métropole']:
            ca_base = random.uniform(3500000, 12000000)
            perf = {
                'Territoire': territoire,
                'Type': 'Métropole',
                'Chiffre_affaires': ca_base,
                'Croissance': random.uniform(2, 12),
                'Magasins': len(self.stores[territoire]),
                'Satisfaction': random.uniform(3.9, 4.5),
                'Part_marche': random.uniform(6, 22),
                'Rentabilité': random.uniform(12, 20),
                'Nouveaux_clients_mois': random.randint(1500, 4000),
                'Panier_moyen': random.uniform(50, 80)
            }
            performance.append(perf)
        
        return pd.DataFrame(performance)
    
    def generate_real_transactions(self, n_transactions=100):
        """Génère des transactions réalistes avec plus de variété"""
        transactions = []
        
        all_territoires = (
            self.territoires['DROM'] + 
            self.territoires['COM'] + 
            self.territoires['Métropole']
        )
        
        transaction_categories = {
            'Vente': ['Alimentation', 'Bricolage', 'Textile', 'Électronique', 'Maison', 'Auto'],
            'Achat': ['Stock Alimentation', 'Stock Bricolage', 'Stock Textile', 'Équipement'],
            'Service': ['Livraison', 'Installation', 'Maintenance', 'SAV'],
            'Frais': ['Loyer', 'Énergie', 'Personnel', 'Marketing']
        }
        
        for i in range(n_transactions):
            days_ago = random.randint(0, 45)
            transaction_date = datetime.now() - timedelta(
                days=days_ago, 
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            territoire = random.choice(all_territoires)
            store = random.choice(self.stores[territoire])
            
            # Catégorie de transaction
            category = random.choice(list(transaction_categories.keys()))
            subcategory = random.choice(transaction_categories[category])
            
            # Montant réaliste selon la catégorie
            if category == 'Vente':
                amount = self._get_sale_amount(subcategory, territoire)
                trans_type = f"Vente {subcategory}"
            elif category == 'Achat':
                amount = -self._get_purchase_amount(subcategory, territoire)
                trans_type = f"Achat {subcategory}"
            elif category == 'Service':
                amount = random.uniform(50, 2000)
                trans_type = f"Service {subcategory}"
            else:  # Frais
                amount = -random.uniform(1000, 15000)
                trans_type = f"Frais {subcategory}"
            
            transactions.append({
                'Date': transaction_date.strftime('%d/%m/%Y %H:%M'),
                'Type': trans_type,
                'Catégorie': category,
                'Magasin': store,
                'Montant': f"{amount:+,.2f} €",
                'Territoire': territoire,
                'Type_Territoire': self._get_territory_type(territoire),
                'ID_Transaction': f"GBH{random.randint(10000, 99999)}"
            })
        
        transactions.sort(key=lambda x: x['Date'], reverse=True)
        return transactions[:n_transactions]
    
    def _get_territory_type(self, territoire):
        """Retourne le type de territoire"""
        if territoire in self.territoires['DROM']:
            return 'DROM'
        elif territoire in self.territoires['COM']:
            return 'COM'
        else:
            return 'Métropole'
    
    def _get_sale_amount(self, department, territoire):
        """Retourne des montants de vente réalistes"""
        base_amounts = {
            'Alimentation': (45, 280),
            'Bricolage': (75, 750),
            'Textile': (30, 220),
            'Électronique': (150, 3000),
            'Maison': (40, 450),
            'Auto': (120, 1500)
        }
        min_val, max_val = base_amounts.get(department, (70, 700))
        
        # Ajustement territorial
        multiplier = 1.0
        if territoire in self.territoires['DROM']:
            multiplier = random.uniform(1.15, 1.35)
        elif territoire in self.territoires['COM']:
            multiplier = random.uniform(1.25, 1.5)
        
        return random.uniform(min_val, max_val) * multiplier
    
    def _get_purchase_amount(self, department, territoire):
        """Retourne des montants d'achat réalistes"""
        base_amounts = {
            'Stock Alimentation': (2500, 35000),
            'Stock Bricolage': (4000, 50000),
            'Stock Textile': (1200, 25000),
            'Équipement': (10000, 80000)
        }
        min_val, max_val = base_amounts.get(department, (3000, 40000))
        
        multiplier = 1.0
        if territoire in self.territoires['DROM']:
            multiplier = random.uniform(1.2, 1.45)
        elif territoire in self.territoires['COM']:
            multiplier = random.uniform(1.3, 1.6)
        
        return random.uniform(min_val, max_val) * multiplier
    
    def get_store_statistics(self):
        """Retourne les statistiques avancées des magasins"""
        stats = []
        for ter_type, territoires in self.territoires.items():
            total_stores = sum(len(self.stores[t]) for t in territoires)
            total_ca = sum(self.generate_territory_performance()[
                self.generate_territory_performance()['Type'] == ter_type
            ]['Chiffre_affaires'])
            
            stats.append({
                'Type': ter_type,
                'Nombre_Territoires': len(territoires),
                'Nombre_Magasins': total_stores,
                'CA_Total': total_ca,
                'CA_Moyen_Par_Magasin': total_ca / total_stores,
                'Magasins_Par_Territoire': total_stores / len(territoires),
                'Performance_Relative': random.uniform(0.8, 1.2)
            })
        return pd.DataFrame(stats)
    
    def get_kpi_summary(self):
        """Retourne un résumé des KPI pour le header"""
        territory_data = self.generate_territory_performance()
        
        return {
            'total_territoires': len(self.territoires['DROM']) + len(self.territoires['COM']) + len(self.territoires['Métropole']),
            'total_magasins': sum(len(magasins) for magasins in self.stores.values()),
            'ca_total_drom': territory_data[territory_data['Type'] == 'DROM']['Chiffre_affaires'].sum(),
            'ca_total_com': territory_data[territory_data['Type'] == 'COM']['Chiffre_affaires'].sum(),
            'ca_total_metro': territory_data[territory_data['Type'] == 'Métropole']['Chiffre_affaires'].sum(),
            'satisfaction_moyenne': territory_data['Satisfaction'].mean(),
            'croissance_moyenne': territory_data['Croissance'].mean()
        }